from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connections

from rcc2.utils import dictfetchall, crad_to_varian_coords

from .models import TreatmentPosition

def index(request):
    return render(request, 'shifty/index.html')

def list(request):
    with connections['crad'].cursor() as cursor:
        cursor.execute("SELECT * FROM Patient ORDER BY Name")
        patients = dictfetchall(cursor)

    #take out any non-numeric MRNs
    clean_patients = []
    for pt in patients:
        if pt['Patient_ID'].isdigit():
            clean_patients.append(pt)

    return render(request, 'shifty/list.html', {'patients': clean_patients})

def add_form(request):
    return render(request, 'shifty/add_form.html')

def add(request):
    patient_mrn = request.POST['mrn']
    patient_date = request.POST['date']

    try:
        result = TreatmentPosition.objects.filter(mrn__exact=patient_mrn).filter(date__exact=patient_date)[0]
        result.vert = request.POST['vert']
        result.long = request.POST['long']
        result.lat = request.POST['lat']
        result.save()
    except IndexError:
        pos = TreatmentPosition.objects.create(
            mrn = request.POST['mrn'],
            date = request.POST['date'],
            vert = request.POST['vert'],
            long = request.POST['long'],
            lat = request.POST['lat']
        )

    if 'submitagain' in request.POST:
        return render(request, 'shifty/add_form.html', {'mrn': request.POST['mrn']})

    return HttpResponseRedirect(reverse('shifty:index'))

def view_patient(request, mrn):
    with connections['crad'].cursor() as cursor:
        cursor.execute(
            """SELECT PatientSession.PatientSessionID FROM PatientSession
            INNER JOIN Patient ON Patient.PatientID = PatientSession.PatientID
            WHERE Patient.Patient_ID=%s
            ORDER BY PatientSession.CreatedOn DESC""",
            [mrn]
        )
        sessionIDs = cursor.fetchall()
        finalPositions = []
        for sessionID in sessionIDs:
            cursor.execute(
                """SELECT PositionResult.PositionResultID, PositionResult.LiveImageID FROM PositionResult
                INNER JOIN Image ON Image.ImageID = PositionResult.LiveImageID
                WHERE PositionResult.PatientSessionID=%s
                ORDER BY Image.CreatedOn DESC""",
                [sessionID[0]]
            )
            positionResults = cursor.fetchall()
            if positionResults:
                #crad coordinates
                final_pos_sql = "SELECT TOP 1 CreatedOn, CouchVert, CouchLong, CouchLat FROM Image where ImageID='"+positionResults[0][1]+"'"
                for pr in positionResults[1:]:
                    final_pos_sql += " OR ImageID="+"'"+pr[1]+"'"
                final_pos_sql += " ORDER BY CreatedOn DESC"
                cursor.execute(final_pos_sql)
                pos = cursor.fetchone()

                #imaging coordinates
                try:
                    imagingPos = TreatmentPosition.objects.filter(mrn__exact=mrn).filter(date__exact=pos[0])[0]
                    ipos = (imagingPos.vert, imagingPos.long, imagingPos.lat)
                except IndexError:
                    ipos = (None, None, None)

                #original coordinates
                relativeShifts = []
                for pr in positionResults:
                    cursor.execute("SELECT NonRigidPositionResult.TranslationX, NonRigidPositionResult.TranslationY, NonRigidPositionResult.TranslationZ FROM NonRigidPositionResult WHERE NonRigidPositionResult.PositionResultID=%s", [pr[0]])
                    shifts = cursor.fetchone()
                    relativeShifts.append((shifts[0],shifts[1],shifts[2]))
                abs_lat = (-1*relativeShifts[0][0]) + pos[3]
                abs_long = (-1*relativeShifts[0][1]) + pos[2]
                abs_vert = (-1*relativeShifts[0][2]) + pos[1]
                for shift in relativeShifts[1:]:
                    abs_lat -= (-1*shift[0])
                    abs_long -= (-1*shift[1])
                    abs_vert -= (-1*shift[2])

                finalPositions.append({
                    'date': pos[0],
                    'initial': crad_to_varian_coords(abs_vert, abs_long, abs_lat),
                    'crad': crad_to_varian_coords(pos[1], pos[2], pos[3]),
                    'imaging': ipos
                })

        cursor.execute("SELECT Name FROM Patient WHERE Patient_ID=%s",[mrn])
        name = cursor.fetchone()

    return render(request, 'shifty/view_patient.html', {'name':name[0], 'mrn':mrn, 'finalPositions':finalPositions})

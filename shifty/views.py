from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import connections

from .models import TreatmentPosition

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def crad_to_varian_coords(vert, long, lat):
    vvert = round(-1*vert/10,1)
    vlong = round(long/10,1)
    if lat < 0:
        vlat = round((10000+lat)/10,1)
    else:
        vlat = round(lat,1)
    return (vvert, vlong, vlat)

def crad_to_varian_coords(coords):
    return crad_to_varian_coords(*coords)

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
    patient_date = request.DATE['date']

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
        cursor.execute("SELECT PatientID FROM Patient WHERE Patient_ID=%s",[mrn])
        patientID = cursor.fetchone()
        cursor.execute("SELECT PatientSessionID FROM PatientSession WHERE PatientID=%s ORDER BY CreatedOn DESC",[patientID[0]])
        sessionIDs = cursor.fetchall()
        finalPositions = []
        for sessionID in sessionIDs:
            cursor.execute("SELECT PositionResultID, LiveImageID FROM PositionResult WHERE PatientSessionID=%s",[sessionID[0]])
            positionResults = cursor.fetchall()
            final_pos_sql = "SELECT TOP 1 CreatedOn, CouchVert, CouchLong, CouchLat FROM Image where ImageID='"+positionResults[0][1]+"'"
            for pr in positionResults[1:]:
                final_pos_sql += " OR ImageID="+"'"+pr[1]+"'"
            final_pos_sql += " ORDER BY CreatedOn DESC"
            cursor.execute(final_pos_sql)
            pos = cursor.fetchone()

            try:
                imagingPos = TreatmentPosition.objects.filter(mrn__exact=mrn).filter(date__exact=pos[0])[0]
                ipos = (imagingPos.vert, imagingPos.long, imagingPos.lat)
            except IndexError:
                ipos = (0,0,0)

            finalPositions.append({
                'date': pos[0],
                'crad': crad_to_varian_coords(pos[1], pos[2], pos[3]),
                'imaging': ipos
            })
        cursor.execute("SELECT Name FROM Patient WHERE Patient_ID=%s",[mrn])
        name = cursor.fetchone()

    return render(request, 'shifty/view_patient.html', {'name':name[0], 'mrn':mrn, 'finalPositions':finalPositions})

from django.shortcuts import render
from django.http import HttpResponse

import requests, json

def list(request):
    s = requests.Session()
    s.post("http://10.110.121.150/auth/login", {'username':'kevin','password':'physics'})

    results = s.get("http://10.110.121.150/_plan/list?sort=date&descending=1&limit=25").json()

    patients = []
    for pt in results['patients']:
        patients.append({'name':pt['patientName'], 'mrn':pt['patientId']})

    return render(request, 'mobiusutils/list.html', {'patients':patients})

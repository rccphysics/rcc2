from django.db import models

class TreatmentPosition(models.Model):
    mrn = models.IntegerField()
    date = models.DateField()
    vert = models.DecimalField(max_digits=4, decimal_places=1)
    long = models.DecimalField(max_digits=4, decimal_places=1)
    lat = models.DecimalField(max_digits=4, decimal_places=1)

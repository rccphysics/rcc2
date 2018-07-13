from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

    class Meta:
        abstract = True

class Doctor(Employee):
    pass

class Dosimetrist(Employee):
    pass

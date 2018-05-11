from django.db import models

class QaTest(models.Model):
    label = models.CharField(max_length=200)
    required = models.BooleanField()
    complete_date = models.DateTimeField('completed on')
    personnel = models.CharField('completed by', max_length=200)
    tp_required = models.BooleanField()
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.label
        
class AverageTest(QaTest):
    #numbers = models.ManyToManyField(NumberTest)
    pass

class NumberTest(QaTest):
    number = models.DecimalField(max_digits=10, decimal_places=3)
    
class CheckboxTest(QaTest):
    checked = models.BooleanField()
    
class QaGroup(models.Model):
    pass
    
class QaTab(models.Model):
    pass
    
class QaSet(models.Model):
    pass

class QaTask(models.Model):
    pass

class Device(models.Model):
    pass
    
class Tool(models.Model):
    pass
    
class Site(models.Model):
    pass

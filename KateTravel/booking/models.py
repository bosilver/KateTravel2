from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank = True)
    comment = models.TextField()

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=300)
    during_time = models.CharField(max_length=50)
    web_adult = models.DecimalField(max_digits=6, decimal_places=2)
    web_child = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    KTL_adult = models.DecimalField(max_digits=6, decimal_places=2)
    KTL_child = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    deposit = models.BooleanField(default=False)
    deposit_adult = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    deposit_child = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    location = models.ForeignKey('Location')

    def __unicode__(self):
        return self.name

class TimeTable(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    timeslot = models.TextField()

    def __unicode__(self):
        return self.activity.name


from django.db import models
from django.utils.translation import gettext as _
# Create your models here.

class Contactus(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    mobino = models.CharField(max_length=12)
    subject = models.TextField()
    msg = models.TextField()
    date = models.DateField()
    def __str__(self):
        return self.name

class BTC(models.Model):
    Date = models.DateField(_("Date"), auto_now=True)
    #Open,High,Low,Close,Adj Close,Volume
    Open = models.FloatField(_("Open"))
    High = models.FloatField(_("High"))
    Low = models.FloatField(_("Low"))
    Close = models.FloatField(_("Close"))
    Volume = models.FloatField(_("Volume"))

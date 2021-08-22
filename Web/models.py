from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    
    user = models.ForeignKey(User)
    coin_name = models.CharField(max_length=25)
    amount = models.FloatField()
    date = models.DateField()

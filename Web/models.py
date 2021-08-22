from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Asset(models.Model):

    user = models.ForeignKey(User,on_delete=CASCADE)
    coin_name = models.CharField(max_length=25)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.user,self.coin_name)

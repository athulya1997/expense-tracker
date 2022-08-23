from django.db import models

# Create your models here.
class login(models.Model):
    name=models.CharField(max_length=20)
    amount=models.CharField(max_length=10)
    password=models.CharField(max_length=10)


class amoundspen(models.Model):
    nname=models.CharField(max_length=30)
    thing=models.CharField(max_length=20)
    price=models.CharField(max_length=30)


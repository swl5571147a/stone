from django.db import models

class Host(models.Model):
    '''store host infomation'''
    hostname = models.CharField(max_length=30)
    osver = models.CharField(max_length=30)
    vender = models.CharField(max_length=30)
    product = models.CharField(max_length=30)
    cpu_model = models.CharField(max_length=30)
    cpu_num = models.IntegerField(max_length=2)
    memory = models.IntegerField(max_length=8)
    sn = models.CharField(max_length=30)
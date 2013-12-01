from django.db import models

# Create your models here.
class Host(models.Model):
    """ store host infomatuion """
    hostname = models.CharField(max_length=30)
    osver = models.CharField(max_length=30)
    vender = models.CharField(max_length=30)
    product = models.CharField(max_length=30)
    cpu_model = models.CharField(max_length=30)
    cpu_num = models.IntegerField(max_length=2)
    memory = models.IntegerField(max_length=8)
    sn = models.CharField(max_length=30)

class IPaddr(models.Model):
    ipaddr = models.IPAddressField()
    host = models.ForeignKey('Host')

class  HostGroup(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(Host)

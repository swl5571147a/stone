from models import Host,IpAddr
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
    list_display = ['vender','product','osver','cpu_model','cpu_num','sn','hostname','memory']

class IpAddrAdmin(admin.ModelAdmin):
    list_display = ['ipaddr','host']

admin.site.register(Host,HostAdmin)
admin.site.register(IpAddr,IpAddrAdmin)
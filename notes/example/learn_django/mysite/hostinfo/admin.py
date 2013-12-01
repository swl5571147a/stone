from models import Host,IpAddr,HostGroup
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
    list_display = ['vender','product','osver','cpu_model','cpu_num','sn','hostname','memory']

class IpAddrAdmin(admin.ModelAdmin):
    list_display = ['ipaddr','host']

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Host,HostAdmin)
admin.site.register(IpAddr,IpAddrAdmin)
admin.site.register(HostGroup,HostGroupAdmin)
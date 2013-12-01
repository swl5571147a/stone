from models import Host,IPaddr,HostGroup
from django.contrib import admin

# Register your models here.
class HostAdmin(admin.ModelAdmin):
    list_display = ['vender',
        'product',
        'osver',
        'cpu_model',
        'cpu_num',
        'sn',
        'hostname'
        ]

class IPaddrAdmin(admin.ModelAdmin):
    list_display = ['ipaddr','host']

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ['name',]

admin.site.register(Host,HostAdmin)
admin.site.register(IPaddr,IPaddrAdmin)
admin.site.register(HostGroup,HostGroupAdmin)

from models import Host
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
    list_display = ['vender','product','osver','cpu_model','cpu_num','sn','hostname','memory']

admin.site.register(Host,HostAdmin)

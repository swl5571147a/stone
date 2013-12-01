from django.shortcuts import render_to_response
from django.http import HttpResponse
from hostinfo.models import Host,IPaddr,HostGroup
try:
    import json
except ImportError,e: 
    import simplejson as json

def collect(request):
    req = request
    if req.POST:
        vender = req.POST.get('vender')
        product = req.POST.get('product')
        cpu_model = req.POST.get('cpu_model')
        cpu_num = req.POST.get('cpu_num')
        memory = req.POST.get('memory')
        sn = req.POST.get('sn')
        osver = req.POST.get('osver')
        hostname = req.POST.get('hostname')
        ipaddrs = req.POST.get('ipaddrs')

        host = Host()
        host.vender = vender
        host.product = product
        host.cpu_model = cpu_model
        host.cpu_num = int(cpu_num)
        host.memory = int(memory)
        host.sn = sn
        host.osver = osver
        host.hostname = hostname
        host.save()

        for ip in ipaddrs.split(':'):
            o_ip = IPaddr()
            o_ip.ipaddr = ip
            o_ip.host = host
            o_ip.save()

        return HttpResponse('ok')
    else:
        return HttpResponse('no post data')

def gethosts(req):
    ret = []
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        ret_hg = {'hostgroup':hg.name,'members':[]}
        members = hg.members.all()
        for h in members:
            ret_h = {'hostname':h.hostname,
                 'ipaddr':[i.ipaddr for i in h.ipaddr_set.all()]
                }
            ret_hg['members'].append(ret_h)
        ret.append(ret_hg)
    ret_status = {'status':0,'data':ret,'message':'ok'}
    return HttpResponse(json.dumps(ret_status))


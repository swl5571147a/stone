from django.shortcuts import render_to_response
from django.template import loader,Context
from django.http import HttpResponse
from testdb.models import Note
# Create your views here.

def index(request):
    n1 = Note(os='linux6',sn='Dell')
    n1.save()
    note = Note.objects.all()
    return render_to_response('contents.html',locals())

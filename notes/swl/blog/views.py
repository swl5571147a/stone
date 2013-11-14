# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def get_file(file_name):
	fopen = open(file_name,'r')
	f = fopen.read()
	fopen.close()
	return f

file_cont = get_file('/var/log/apache2/access.log')

def index(reg):
#	return HttpResponse('<h1>Hello World!</h1><pre><p>%s</p></pre>'%file_cont)
	return render(reg,'index.html',{'f':file_cont,'test':'This is test!'})

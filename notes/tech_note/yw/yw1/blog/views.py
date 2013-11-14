from django.http import HttpResponse
from django.shortcuts import render

FILE_DIR = '/etc/passwd'

def index(req):
    fp = open(FILE_DIR, 'r')
    s = fp.read()
    fp.close()
    #return HttpResponse("<h1>hello world!!</h1><pre><p>%s</p></pre>"%s)
    return render(req, 'a.tpl', {'s':s, 'title':'file conte', 'a1':{}})


def index1(req):
    s = "this is url from a"
    #return HttpResponse("<h1>hello world!!</h1><pre><p>%s</p></pre>"%s)
    return render(req, 'a.tpl', {'s':s, 'title':'file conte', 'a1':{}})

def index2(req):
    s = "from b"
    #return HttpResponse("<h1>hello world!!</h1><pre><p>%s</p></pre>"%s)
    return render(req, 'a.tpl', {'s':s, 'title':'file conte', 'a1':{}})

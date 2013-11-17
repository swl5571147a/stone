from django.template import loader,Context
from django.http import HttpResponse



def index(request):
    d = {
         'name':'swl',
         'age':24,
         'sex':'male'
        }
    t = loader.get_template('content.html')
    c = Context({'ss':d})
    return HttpResponse(t.render(c))



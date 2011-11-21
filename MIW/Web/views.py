from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from Web.models import operador, alerta

# Create your views here.
def index(request):
    return render_to_response('skel/index.html')

def alertas(request):
    object_list = alerta.objects.order_by('-enviado')[:10]
    return render_to_response('skel/alerta_list.html',
                              {'object_list': object_list})

def detail(request, object_id):
    alerta = get_object_or_404(alerta, pk=alerta_id)
    return render_to_response('skel/alerta_detail.html',
                              {'object': alerta})

def about(request):
    return HttpResponse("About")
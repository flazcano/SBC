from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from Web.models import operador, alerta

# Create your views here.
def index(request):
    return render_to_response('skel/index.html')

def about(request):
    return HttpResponse("About")

def alertas(request):
    listadealertas = alerta.objects.all()
    return render_to_response('skel/alertas.html', {'alertas': listadealertas})

def detallealerta(request, id):
    unaalerta = get_object_or_404(alerta, pk=id)
    return render_to_response('skel/detallealerta.html', {'alerta': unaalerta})

def servidores(request):
    listadeservidores = sbc.alerta.objects.all()
    return render_to_response('skel/alertas.html', {'alertas': listadealertas})


def detallealertasoperador(request, opid):
    alertas = get_object_or_404(alerta, opid)
    return render_to_response('skel/alertas_operador.html', {'object': alertas})
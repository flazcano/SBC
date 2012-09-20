from django.http import HttpResponse, HttpResponseRedirect
from Web.instalar import run

def instalar(request):
    miInstalacion = run()
    miInstalacion.crear_admingroup()
    miInstalacion.crear_admin()
    miInstalacion.crear_appgroup()
    miInstalacion.crear_appgroup_add()
    miInstalacion.crear_appgroup_change()
    miInstalacion.crear_appgroup_delete()
    return HttpResponseRedirect("/admin/Web/")
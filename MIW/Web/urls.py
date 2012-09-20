from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MIW.Web.views.index',),
    url(r'^about', 'MIW.Web.views.about',),
    url(r'^alertas', 'MIW.Web.views.alertas',),
    url(r'^alertas/detalle/(?P<id>\d+)/$', 'MIW.Web.views.detallealerta',),
    url(r'^servidor', 'MIW.Web.views.servidor',),
)
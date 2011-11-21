from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MIW.Web.views.index', name='index'),
    url(r'^about', 'MIW.Web.views.about', name='about'),
    url(r'^alertas', 'MIW.Web.views.alertas', name='alertas'),
)
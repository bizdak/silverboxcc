from django.conf.urls import url
from . import views

urlpatterns = [
    url('^stbi$', views.stbi, name='stbi'),
    url('^sban$', views.sban, name='sban'),
    url('^sy', views.sy, name='sban'),
    url('^ssl', views.ssl, name='sban'),
    url('^scal', views.scal, name='scal'),
    url('^scol', views.scol, name='scol'),
    url('^ucs', views.ucs, name='ucs'),
    url(r'^bots/(?P<bot_id>[0-9]+)', views.bots, name='bots'),
    url('^sendcommand/(?P<bot_id>[0-9]+)', views.send_command, name='sendcommand'),
    url('^deletedata/(?P<bot_id>[0-9]+)/(?P<data_id>[a-z]+)', views.deletedata, name='deletedata'),
    url('^$', views.index, name='index'),
]

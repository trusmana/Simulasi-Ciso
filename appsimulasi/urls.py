from django.conf.urls import url
from django.views import generic
from appsimulasi import views

app_name = 'appsimulasi'

urlpatterns = [
    url(r'^val_retensi/$',views.val_retensi,name='val_retensi'),
    url(r'^hitung_mutasi/$',views.hitung_mutasi,name='hitung_mutasi'),
    url(r'^simulasi/$',views.index, name='simulasi'),
    url(r'^cek_usia/$', views.cek_usia, name='cek_usia'),
    url(r'^maks_plafond/$', views.maks_plafond, name='maks_plafond'),
    url(r'^show_simulasi/$', views.show_simulasi, name='show_simulasi'),

    ]

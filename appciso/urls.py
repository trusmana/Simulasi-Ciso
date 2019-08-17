from django.conf.urls import url,include
from django.contrib import admin
from core import views as core_views
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    url(r'^', include('appsimulasi.urls', namespace='simulasi')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT})
]

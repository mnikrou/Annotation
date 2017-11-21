from django.conf.urls import url
from django.contrib import admin
from Annotation import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^draw/', views.draw, name='draw'),
]
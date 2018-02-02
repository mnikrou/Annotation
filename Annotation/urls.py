from django.conf.urls import url
from django.contrib import admin
from Annotation import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, kwargs={'next_page': '/'}, name='logout'),
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^cpanel/', views.cpanel, name='cpanel'),
    url(r'^draw/', views.draw, name='draw'),
    url(r'^images/', views.images, name='images'),
    url(r'^upload/img/$', views.upload_image, name='upload_image'),
    url(r'^get_image/$', views.get_image, name='get_image'),
    url(r'^load_images/$', views.load_images, name='load_images'),
    url(r'^delete_image/$', views.delete_image, name='delete_image'),
    url(r'^save_annotation/$', views.save_annotation, name='save_annotation'),
]

if settings.DEBUG is True:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
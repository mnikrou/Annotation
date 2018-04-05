from django.conf.urls import url
from django.contrib import admin
from Annotation import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Annotation import draw_views, analysis_views

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
    url(r'^get_image/$', draw_views.get_image, name='get_image'),
    url(r'^load_images/$', views.load_images, name='load_images'),
    url(r'^delete_image/$', views.delete_image, name='delete_image'),
    url(r'^save_annotation/$', draw_views.save_annotation, name='save_annotation'),
    url(r'^analysis/(?P<image_id>.+)/$', analysis_views.analysis, name='analysis'),
    url(r'^get_user_annotation/$', analysis_views.get_user_annotation, name='get_user_annotation'),
    url(r'^user_directory_delete/$', views.user_directory_delete, name='user_directory_delete'),
    url(r'^delete_directory/$', views.delete_directory, name='delete_directory'),
    url(r'^all_user_analysis/(?P<image_id>.+)/$', analysis_views.all_user_analysis, name='all_user_analysis'),
    url(r'^get_user_geds/$', analysis_views.get_user_geds, name='get_user_geds'),
    url(r'^calculate_user_ged/$', views.calculate_user_ged, name='calculate_user_ged'),
    url(r'^calculateGeds/$', views.calculateGeds, name='calculateGeds'),
]

if settings.DEBUG is True:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
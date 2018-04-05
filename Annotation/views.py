from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ImageUploadForm
from .models import *
from django.core import serializers
from .images import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.core.exceptions import ObjectDoesNotExist
from .utils import *
from django.conf import settings
import os
from PIL import Image as PImage
import shutil
from GraphEditDistance.Graph.graph import *
import GraphEditDistance.graph_edit_distance as ged


def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())


@login_required
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


@login_required
def draw(request):
    template = loader.get_template('draw.html')
    ajax_url = re.sub('/draw/', '', request.path)
    if is_expert_user(request.user):
        images = Image.objects.all()
    else:
        annotated_image_ids = ImageAnnotation.objects.filter(
            user__groups__name='EXPERT_USERS').values_list('image')
        images = Image.objects.filter(id__in=annotated_image_ids)
    c = {'imagesCount': images.count(), 'ajaxUrl': ajax_url}
    return HttpResponse(template.render(c, request))


@login_required
def cpanel(request):
    template = loader.get_template('cpanel.html')
    c = {}
    return HttpResponse(template.render(c, request))


@login_required
def images(request):
    template = loader.get_template('images.html')
    ajax_url = re.sub('/images/', '', request.path)
    c = {'ajaxUrl': ajax_url}
    return HttpResponse(template.render(c, request))


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Image(img=form.cleaned_data['image'])
            m.save()
        return redirect('images')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


@login_required
@permission_required('Annotation.add_image', raise_exception=True)
def load_images(request):
    if request.is_ajax():
        images = get_image_by_page_number(
            int(request.POST['page_number']), 10, request.user)
        imgaesHtml = ''
        ajax_url = re.sub('/load_images/', '', request.path)
        for rec in images.object_list:
            imgaesHtml += '<div class=\"show-image\"><img src="' + rec.img.url + '" alt="" style="width: 250px; height: 250px; margin-bottom: 5px" /><button class="btn btn-primary btn-circle btn-line" style="top:0; left:0;" ><a class="icon-eye-open" href="' + \
                rec.img.url + \
                '"></a></button> <input class="btn btn-danger btn-circle btn-line" type="button" value="X" style="top:0; left:85%;" onclick="deleteImage(' + str(
                    rec.id) + ')\"></input>' +\
                '<button class="btn btn-primary btn-circle btn-line" style="top:0; left:42%;" ><a class="icon-eye-open" href="' + ajax_url + '/analysis/' + str(rec.id) + '"></a></button>' +\
                '</div>'
        response_data = json.dumps(
            {'total_pages': images.paginator.num_pages, 'html': imgaesHtml})
        return HttpResponse(response_data, content_type='application/json')
    return HttpResponseForbidden('allowed only via Ajax')


@login_required
@permission_required('Annotation.delete_image', raise_exception=True)
def delete_image(request):
    if request.is_ajax():
        id = int(request.POST['id'])
        m = Image.objects.get(id=id)
        m.delete()
        return HttpResponse('')
    return HttpResponseForbidden('allowed only via Ajax')


@login_required
def user_directory_delete(request):
    if request.user.username == 'miladn':
        ajax_url = re.sub('/user_directory_delete/', '', request.path)
        users = User.objects.filter(Q(groups__name='EXPERT_USERS'))
        c = {'users': users, 'ajaxUrl': ajax_url}
        return render(request, 'user_directory_delete.html', c)
    else:
        return HttpResponse('not correct user')


@login_required
def delete_directory(request):
    if request.is_ajax():
        if request.user.username == 'miladn':
            dir = settings.MEDIA_ROOT + '/expert_annotated_images/' + \
                request.POST['user_name']
            # if (dir):
            shutil.rmtree(dir)
            return HttpResponse('')
        else:
            return HttpResponse('not correct user')
    return HttpResponseForbidden('allowed only via Ajax')


@login_required
@permission_required('Annotation.add_userged', raise_exception=True)
def calculate_user_ged(request):
    ajax_url = re.sub('/calculate_user_ged/', '', request.path)
    c = {'ajaxUrl': ajax_url}
    return render(request, 'ged_calculation.html', c)


@login_required
def calculateGeds(request):
    if request.is_ajax():
        UserGED.objects.all().delete()
        images = Image.objects.all()
        for img in images:
            expert_ia = ImageAnnotation.objects.filter(
                user__groups__name='EXPERT_USERS', image=img)
            if expert_ia:
                expert_graph = Graph.from_json(
                    json.loads(expert_ia[0].annotation_json))
            crowd_ia_list = ImageAnnotation.objects.filter(Q(user__groups__name='TRAINED_POWER_USERS') | Q(
                user__groups__name='UNTRAINED_POWER_USERS'), image=img)
            for crowd_ia in crowd_ia_list:
                crow_graph = Graph.from_json(
                    json.loads(crowd_ia.annotation_json))
                distance = ged.compareGraphs(expert_graph, crow_graph)
                uged = UserGED(image=img, user=crowd_ia.user, ged=distance)
                uged.save()
        return HttpResponse('')

    return HttpResponseForbidden('allowed only via Ajax')

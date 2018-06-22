from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render
from .images import *
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
import re
from django.conf import settings
import os
from django.contrib.auth.models import User
import json
from GraphEditDistance.Graph.graph import *
import GraphEditDistance.graph_edit_distance as ged
from django.db.models import Avg

user_geds = list()


@login_required
def analysis(request, image_id):
    template = loader.get_template('analyze_annotation.html')
    ajax_url = re.sub('/analysis/' + image_id + '/', '', request.path)
    dir = [name for name in os.listdir(settings.EXPERT_ANNOTATED_IMAGES)]
    if (dir):
        imgUrl = settings.MEDIA_URL + 'expert_annotated_images/' + \
            dir[0] + '/' + str(image_id) + '.png'
    crowd_users = User.objects.filter(
        Q(groups__name='TRAINED_POWER_USERS') | Q(groups__name='UNTRAINED_POWER_USERS'))
    c = {'imageId': int(image_id), 'expert_annotated_image_url': imgUrl,
         'crowd_users': crowd_users, 'ajaxUrl': ajax_url}
    return render(request, 'analyze_annotation.html', c)


@login_required
def get_user_annotation(request):
    if request.is_ajax():
        #ajax_url = re.sub('/analysis/', '', request.path)
        img = Image.objects.filter(id=int(request.POST['imageId']))
        crowd_annotation_json = ''
        res = {}
        imgurl = ''
        crowd_user = User.objects.filter(id=int(request.POST['crowd_user_id']))
        cr_ia = ImageAnnotation.objects.filter(user=crowd_user, image=img)
        distance = -1
        if cr_ia:
            crowd_annotation_json = cr_ia[0].annotation_json
            dir = [name for name in os.listdir(
                settings.CROWD_ANNOTATED_IMAGES)]
            if (dir):
                imgUrl = settings.MEDIA_URL + 'crowd_annotated_images/' + \
                    crowd_user[0].username + '/' + \
                    str(int(request.POST['imageId'])) + '.png'
            ex_ia = ImageAnnotation.objects.filter(
                user__groups__name='EXPERT_USERS', image=img)
            if ex_ia:
                g1 = Graph.from_json(json.loads(ex_ia[0].annotation_json))
                g2 = Graph.from_json(json.loads(crowd_annotation_json))
                distance = ged.compareGraphs(g1, g2)
            res = {'crowd_image_url': imgUrl, 'ged': distance}
        return HttpResponse(json.dumps(res))
    return HttpResponseForbidden('allowed only via Ajax')


@login_required
def all_user_analysis(request, image_id):
    ajax_url = re.sub('/all_user_analysis/' + image_id + '/', '', request.path)
    user_geds = list()
    img = Image.objects.filter(id=image_id)
    expert_ia = ImageAnnotation.objects.filter(
        user__groups__name='EXPERT_USERS', image=img)
    if expert_ia:
        expert_graph = Graph.from_json(
            json.loads(expert_ia[0].annotation_json))
    crowd_ia_list = ImageAnnotation.objects.filter(Q(user__groups__name='TRAINED_POWER_USERS') | Q(
        user__groups__name='UNTRAINED_POWER_USERS'), image=img)
    for crowd_ia in crowd_ia_list:
        crow_graph = Graph.from_json(json.loads(crowd_ia.annotation_json))
        distance = ged.compareGraphs(expert_graph, crow_graph)
        user_geds.append({'user_id': crowd_ia.user_id, 'user_name': crowd_ia.user.username,
                          'user_group': crowd_ia.user.groups.values()[0]['name'], 'disntance': distance})
    c = {'imageId': int(image_id),
         'image_url': img[0].img.url, 'ajaxUrl': ajax_url}
    return render(request, 'analyze_all_users.html', c)


@login_required
def get_user_geds(request):
    if request.is_ajax():
        user_geds = list()
        avg = 0
        img = Image.objects.filter(id=int(request.POST['imageId']))
        if request.POST['userGroup'] == 'all':
            user_geds = UserGED.objects.filter(image=img).values('ged', 'user__username')
            avg = UserGED.objects.filter(image=img).aggregate(Avg('ged'))
        elif request.POST['userGroup'] == 'TRAINED_POWER_USERS':
            user_geds = UserGED.objects.filter(Q(image=img,user__groups__name='TRAINED_POWER_USERS')).values('ged', 'user__username')
            avg = UserGED.objects.filter(Q(image=img,user__groups__name='TRAINED_POWER_USERS')).aggregate(Avg('ged'))
        elif request.POST['userGroup'] == 'UNTRAINED_POWER_USERS':
            user_geds = UserGED.objects.filter(Q(image=img,user__groups__name='UNTRAINED_POWER_USERS')).values('ged', 'user__username')
            avg = UserGED.objects.filter(Q(image=img,user__groups__name='UNTRAINED_POWER_USERS')).aggregate(Avg('ged'))
        response_data = json.dumps(
            {'user_geds': list(user_geds), 'avg': avg['ged__avg']})
        return HttpResponse(response_data)
    return HttpResponseForbidden('allowed only via Ajax')

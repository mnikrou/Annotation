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


@login_required
def analysis(request, image_id):
    template = loader.get_template('analyze_annotation.html')
    ajax_url = re.sub('/analyze_annotation/', '', request.path)
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
        ajax_url = re.sub('/analyze_annotation/', '', request.path)
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

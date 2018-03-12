from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render
from .images import *
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
import re
from django.conf import settings
import os
from django.contrib.auth.models import User


@login_required
def analysis(request, image_id):
    template = loader.get_template('analyze_annotation.html')
    ajax_url = re.sub('/analyze_annotation/', '', request.path)
    dir = [name for name in os.listdir(settings.EXPERT_ANNOTATED_IMAGES)]
    if (dir):
        imgUrl = settings.MEDIA_URL + 'expert_annotated_images/' + \
            dir[0] + '/' + str(image_id) + '.png'
    crowd_users = User.objects.filter(Q(groups__name='TRAINED_POWER_USERS') | Q(groups__name='UNTRAINED_POWER_USERS'))
    c = {'imageId': int(image_id), 'expert_annotated_image_url': imgUrl, 'crowd_users':crowd_users, 'ajaxUrl': ajax_url}
    return render(request, 'analyze_annotation.html', c)

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render
from .images import *
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
import re
from django.conf import settings
import os


@login_required
def analysis(request, image_id):
    template = loader.get_template('analyze_annotation.html')
    ajax_url = re.sub('/analyze_annotation/', '', request.path)
    dir = [name for name in os.listdir(settings.EXPERT_ANNOTATED_IMAGES)]
    if (dir):
        imgUrl = settings.MEDIA_URL + 'expert_annotated_images/' + \
            dir[0] + '/' + str(image_id) + '.png'
    c = {'imageId': int(image_id), 'expert_annotated_image_url': imgUrl, 'ajaxUrl': ajax_url}
    return render(request, 'analyze_annotation.html', c)

from django.http import HttpResponse, HttpResponseForbidden
from .images import *
from django.contrib.auth.decorators import login_required, permission_required
from .utils import *
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import os
from django.conf import settings
import json
from GraphEditDistance.Graph.graph import *
from django.contrib.auth.models import User

TRAINING_IMAGES_DIR = settings.MEDIA_ROOT + "/training_images/"


@login_required
def get_image(request):
    if request.is_ajax():
        annotation_json = ''
        nodes_count = 0
        page_num = int(request.POST['page_num'])
        img = get_image_by_page_number(page_num, 1)
        is_expert = is_expert_user(request.user)
        ia = ImageAnnotation.objects.filter(
            user=request.user, image=img.object_list[0])
        if ia:
            annotation_json = ia[0].annotation_json
        ia2 = ImageAnnotation.objects.filter(
            user__groups__name='EXPERT_USERS', image=img.object_list[0])
        if ia2:
            g = Graph.from_json(json.loads(ia2[0].annotation_json))
            nodes_count = g.size()
        if(not is_expert):
            if (page_num in [1, 2, 3]):
                dir = [name for name in os.listdir(TRAINING_IMAGES_DIR)]
                if (dir):
                    imgUrl = settings.MEDIA_URL + 'training_images/' + \
                        dir[0] + '/' + str(img.object_list[0].id) + '.png'
                    res = {'imageUrl': imgUrl, 'imageId': img.object_list[0].id, 'imgHeight': img.object_list[0].img.height,
                           'imgWidth': img.object_list[0].img.width, 'annotation': annotation_json, 'isExpertUser': is_expert, 'nodesCount': nodes_count}
                    return HttpResponse(json.dumps(res))
        res = {'imageUrl': img.object_list[0].img.url, 'imageId': img.object_list[0].id, 'imgHeight': img.object_list[0].img.height,
               'imgWidth': img.object_list[0].img.width, 'annotation': annotation_json, 'isExpertUser': is_expert, 'nodesCount': nodes_count}
        return HttpResponse(json.dumps(res))
    return HttpResponseForbidden('allowed only via Ajax')


@login_required
def save_annotation(request):
    if request.is_ajax():
        image = Image.objects.get(id=int(request.POST['image_id']))
        g = Graph.from_json(json.loads(request.POST['annotation_json']))
        nodes_count = g.size()
        if int(request.POST['training_nodes_count']) != nodes_count:
            return HttpResponse("You should annotate image with " + request.POST['training_nodes_count'] + " nodes")
        try:
            ia = ImageAnnotation.objects.get(user=request.user, image=image)
        except ObjectDoesNotExist:
            ia = None
        if (ia):
            ia.annotation_json = request.POST['annotation_json']
        else:
            ia = ImageAnnotation(user=request.user, image=image,
                                 annotation_json=request.POST['annotation_json'])
        ia.save()
        if(is_expert_user(request.user)):
            dir = TRAINING_IMAGES_DIR + request.user.username
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(dir + "/" + request.POST['image_id'] + ".png", "wb") as fh:
                fh.write(request.POST['image_url'].replace(
                    'data:image/png;base64,', '').decode('base64'))
        return HttpResponse('')
    return HttpResponseForbidden('allowed only via Ajax')

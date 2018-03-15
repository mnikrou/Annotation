from django.core.paginator import Paginator
from .models import Image, ImageAnnotation
from .utils import *


def get_image_by_page_number(page_num, count, user):
    if not is_crowd_user(user):
        images = Image.objects.order_by('order')
    else:
        annotated_image_ids = ImageAnnotation.objects.filter(
            user__groups__name='EXPERT_USERS').values_list('image')
        images = Image.objects.filter(id__in=annotated_image_ids)
    p = Paginator(images, count)
    img = p.page(page_num)
    return img

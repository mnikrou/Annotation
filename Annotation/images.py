from django.core.paginator import Paginator
from .models import Image

def get_image_by_page_number(page_num, count):
    p = Paginator(Image.objects.all(), count)
    img = p.page(page_num)
    return img

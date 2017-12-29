from django.core.paginator import Paginator
from models import Image

def get_image_by_page_number(page_num):
    p = Paginator(Image.objects.all(), 1)
    img = p.page(page_num)
    return img

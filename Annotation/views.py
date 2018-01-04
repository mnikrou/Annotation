from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import *
from django.core import serializers
from .images import *

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
    img = serializers.serialize('json', Image.objects.all())
    c = {'imagesCount': Image.objects.count()}
    return HttpResponse(template.render(c, request))

@login_required
def cpanel(request):
    template = loader.get_template('cpanel.html')
    c = {}
    return HttpResponse(template.render(c, request))

@login_required
def images(request):
    template = loader.get_template('images.html')
    form = ImageUploadForm(request.POST, request.FILES)
    c = {'images': Image.objects.all(), 'form': form}
    return HttpResponse(template.render(c, request))

@login_required
def save_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Image(img = form.cleaned_data['image'])
            m.save()
            return images(request)
    return HttpResponseForbidden('allowed only via POST')

@login_required
def upload_image(request):
    template = loader.get_template('upload_image.html')
    return HttpResponse(template.render())

@login_required
def get_image(request):
    if request.is_ajax():
        img = get_image_by_page_number(int(request.POST['page_num']))
        #data = serializers.serialize('json', img.object_list[0].img.url)
        return HttpResponse(img.object_list[0].img.url)
    return HttpResponseForbidden('allowed only via Ajax')
    
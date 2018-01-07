from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import *
from django.core import serializers
from .images import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

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
    c = {'images': Image.objects.all()}
    return HttpResponse(template.render(c, request))

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Image(img = form.cleaned_data['image'])
            m.save()
        return redirect('images')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', { 'form': form })

@login_required
def get_image(request):
    if request.is_ajax():
        img = get_image_by_page_number(int(request.POST['page_num']), 1)
        #data = serializers.serialize('json', img.object_list[0].img.url)
        return HttpResponse(img.object_list[0].img.url)
    return HttpResponseForbidden('allowed only via Ajax')
    
@login_required
def load_images(request):
    if request.is_ajax():
        images = get_image_by_page_number(int(request.POST['page_number']), 10)
        #data = serializers.serialize('json', img.object_list[0].img.url)
        return HttpResponse(images.object_list)
    return HttpResponseForbidden('allowed only via Ajax')
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import *
from django.core import serializers
from .images import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import re

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
    ajax_url = re.sub('/draw/', '', request.path)
    c = {'imagesCount': Image.objects.count(), 'ajaxUrl' : ajax_url}
    return HttpResponse(template.render(c, request))

@login_required
def cpanel(request):
    template = loader.get_template('cpanel.html')
    c = {}
    return HttpResponse(template.render(c, request))

@login_required
def images(request):
    template = loader.get_template('images.html')
    ajax_url = re.sub('/images/', '', request.path)
    c = {'ajaxUrl' : ajax_url}
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
        imgaesHtml = ''
        for rec in images.object_list:
            imgaesHtml += '<div class=\"show-image\"><img src="'+rec.img.url+'" alt="" style="width: 250px; height: 250px; margin-bottom: 5px" /><button class="btn btn-primary btn-circle btn-line" style="top:0; left:0;" ><a class="icon-eye-open" href="'+rec.img.url+'"></a></button> <input class="btn btn-danger btn-circle btn-line" type="button" value="X" style="top:0; left:85%;" onclick="deleteImage('+str(rec.id)+')"/> </div>'
        response_data = json.dumps({'total_pages':images.paginator.num_pages , 'html': imgaesHtml})
        return HttpResponse(response_data, content_type='application/json')
    return HttpResponseForbidden('allowed only via Ajax')

@login_required
def delete_image(request):
    if request.is_ajax():
        id = int(request.POST['id'])
        m = Image.objects.get(id=id)
        m.delete()
        return HttpResponse('')
    return HttpResponseForbidden('allowed only via Ajax')
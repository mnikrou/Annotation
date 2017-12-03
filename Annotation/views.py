from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
from .forms import ImageUploadForm
from .models import Image


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
    return HttpResponse(template.render())

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
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Image(img = form.cleaned_data['image'])
            m.save()
            return images(request)
    return HttpResponseForbidden('allowed only via POST')
    
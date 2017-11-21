from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

@login_required
def draw(request):
    template = loader.get_template('draw.html')
    return HttpResponse(template.render())
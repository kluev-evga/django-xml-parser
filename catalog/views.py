from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api.models import Mark


def index(request):
    return render(
        request,
        'index.html',
        {"marks": Mark.objects.all()})


@csrf_exempt
def add_catalog(request):
    return render(request, 'catalog.html')

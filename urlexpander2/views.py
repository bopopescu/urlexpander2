from django.shortcuts import render, get_list_or_404
from .models import Url


def index(request):
    all_urls = Url.objects.all()
    return render(request, 'index.html', {'all_urls': all_urls})

def detail(request, url_id):
    url = get_list_or_404(Url, pk=url_id)
    return render(request, 'detail.html', {'url': url})

#def add(request):

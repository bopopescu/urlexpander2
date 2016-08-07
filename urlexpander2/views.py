from django.shortcuts import render, get_list_or_404
from .models import Url


def index(request):
    all_urls = Url.objects.all()
    return render(request, 'index.html', {'all_urls': all_urls})

#def detail(request, album_id):
 #   album = get_list_or_404(Album, pk=album_id)
  #  return render(request, 'music/detail.html', {'album': album,})

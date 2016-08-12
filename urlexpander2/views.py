from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from .models import Url
import requests, bs4

def index(request):
    urls = Url.objects.all()
    return render(request, 'urlexpander2/index.html', {'all_urls': urls})

class DetailView(generic.DetailView):
    model = Url
    template_name = 'urlexpander2/detail.html'

def add_url(request):
    new_url = Url()
    shortened_url = request.POST['new_url']
    r = requests.get(shortened_url)
    beautiful = bs4.BeautifulSoup(r.text)
    new_url.shortened = shortened_url
    new_url.title = beautiful.title.text
    new_url.destination = r.url
    new_url.status = r.status_code
    new_url.save()
    return render(request, 'urlexpander2/detail.html', {'url':new_url})

class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']
    template_name_suffix = '_update_form'

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('index')












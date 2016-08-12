from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from .models import Url
import requests, bs4, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def index(request):
    urls = Url.objects.all()
    return render(request, 'urlexpander2/index.html', {'all_urls': urls})

@login_required
def detail(request, pk):
    url = Url.objects.get(pk=pk)
    return render(request, 'urlexpander2/detail.html', {'url': url})

@login_required
def add_url(request):
    new_url = Url()
    shortened_url = request.POST['new_url']
    r = requests.get(shortened_url)
    beautiful = bs4.BeautifulSoup(r.text)
    new_url.shortened = shortened_url
    new_url.title = beautiful.title.text
    new_url.destination = r.url
    new_url.status = r.status_code

    arch_url = 'http://archive.org/wayback/available?url=' + shortened_url
    checked = requests.get(arch_url)
    data = json.loads(checked.text)
    snapshot = data['archived_snapshots']['closest']['url']
    timestamp = data['archived_snapshots']['closest']['timestamp']
    new_url.snapshot_url = snapshot
    new_url.timestamp = timestamp

    new_url.save()
    return render(request, 'urlexpander2/detail.html', {'url':new_url})

@login_required
def logout_view(request):
    logout(request)
    return redirect('urlexpander2/index.html')


class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']
    template_name_suffix = '_update_form'

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('index')












from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from .models import Url
from .forms import UserForm
import requests, bs4, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/urlexpander/accounts/login/')
def index(request):
    urls = Url.objects.all()
    return render(request, 'urlexpander2/index.html', {'all_urls': urls})

@login_required(login_url='/urlexpander/accounts/login/')
def detail(request, pk):
    url = Url.objects.get(pk=pk)
    return render(request, 'urlexpander2/detail.html', {'url': url})

@login_required(login_url='/urlexpander/accounts/login/')
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

# @login_required(login_url='/urlexpander2/login', redirect_field_name='url-update')
class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']
    template_name_suffix = '_update_form'

# @login_required(login_url='/urlexpander2/login', redirect_field_name='url-delete')
class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('urlexpander2:index')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('urlexpander2:index')
    return render(request, 'registration/login.html', {'error_message': 'Invalid login'})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'registration/login.html', context)










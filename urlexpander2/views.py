from django.shortcuts import render, redirect, get_object_or_404
from .models import Url
from .forms import UserForm, UrlEditForm
from mysite.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import requests, bs4, json
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/urlexpander2/accounts/login/')
def index(request):
    urls = Url.objects.all()
    return render(request, 'urlexpander2/index.html', {'all_urls': urls})

@login_required(login_url='/urlexpander2/accounts/login/')
def detail(request, pk):
    url = Url.objects.get(pk=pk)
    return render(request, 'urlexpander2/detail.html', {'url': url})

@login_required(login_url='/urlexpander2/accounts/login/')
def add_url(request):
    new_url = Url()
    shortened_url = request.POST['new_url']
    r = requests.get(shortened_url)
    beautiful = bs4.BeautifulSoup(r.text)
    new_url.shortened = shortened_url
    new_url.title = beautiful.title.text
    new_url.destination = r.url
    new_url.status = r.status_code

    #wayback
    arch_url = 'http://archive.org/wayback/available?url=' + shortened_url
    checked = requests.get(arch_url)
    data = json.loads(checked.text)
    snapshot = data['archived_snapshots']['closest']['url']
    timestamp = data['archived_snapshots']['closest']['timestamp']
    new_url.snapshot_url = snapshot
    new_url.timestamp = timestamp

    #S3
    api_key = 'ak-cyywv-37en6-w9yr4-3df7w-7ygkz'
    response = '{url:"'+ snapshot + '",renderType:"jpg",outputAsJson:false}'
    url = 'http://PhantomJsCloud.com/api/browser/v2/' + api_key + '/?request=' + response
    resource = requests.get(url)
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    mybucket = conn.get_bucket('lab3images')
    k = Key(mybucket)
    k.key = new_url.pk
    k.set_contents_from_string(resource.content)
    new_url.screenshot_url = url
    new_url.save()
    return render(request, 'urlexpander2/detail.html', {'url':new_url})

@login_required(login_url='/urlexpander2/accounts/login/')
def UrlUpdate(request, pk):
    if request.method != 'POST':
        url = get_object_or_404(Url, pk=pk)
        form = UrlEditForm(initial={'shortened': url.shortened,
                                    'destination': url.destination,
                                    'status': url.status,
                                    'title': url.title,
                                    'snapshot_url': url.snapshot_url,
                                    'timestamp': url.timestamp})
        return render(request, 'urlexpander2/url_update_form.html', {'form': form})
    else:
        url = get_object_or_404(Url, pk=pk)
        url.shortened = request.POST['shortened']
        url.destination = request.POST['destination']
        url.status = request.POST['status']
        url.title = request.POST['title']
        url.snapshot_url = request.POST['snapshot_url']
        url.timestamp = request.POST['timestamp']
        url.save()
        return redirect('urlexpander2:index')


@login_required(login_url='/urlexpander2/accounts/login/')
def UrlDelete(request, pk):
    url = get_object_or_404(Url, pk=pk)
    url.delete()
    return redirect('urlexpander2:index')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('urlexpander2:index')
    return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'registration/login.html', context)










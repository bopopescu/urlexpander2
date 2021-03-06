from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ratelimit.decorators import ratelimit
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Url
from .forms import UserForm, UrlEditForm
from mysite.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from .serializers import UrlDetailSerializer, UrlListSerializer, UrlAddSerializer

import requests, bs4, json

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
def index(request):
	urls = Url.objects.all()
	return render(request, 'urlexpander2/index.html', {'all_urls': urls})

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
def detail(request, pk):
	url = Url.objects.get(pk=pk)
	return render(request, 'urlexpander2/detail.html', {'url': url})

@ratelimit(key="ip", rate="10/m", block=True)
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

	#phantomJS
	api_key = 'ak-cyywv-37en6-w9yr4-3df7w-7ygkz'
	response = '{url:"'+ snapshot + '",renderType:"jpg",outputAsJson:false}'
	url = 'http://PhantomJsCloud.com/api/browser/v2/' + api_key + '/?request=' + response
	new_url.screenshot_url = url
	new_url.save()

    #S3
	resource = requests.get(url)
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	mybucket = conn.get_bucket('lab3images')
	k = Key(mybucket)
	k.key = new_url.pk
	k.set_contents_from_string(resource.content)
	return render(request, 'urlexpander2/detail.html', {'url':new_url})

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
def UrlUpdate(request, pk):
	if request.method != 'POST':
		url = get_object_or_404(Url, pk=pk)
		form = UrlEditForm(initial={'shortened': url.shortened,
									'destination': url.destination,
									'status': url.status,
									'title': url.title,
									'snapshot_url': url.snapshot_url,
									'timestamp': url.timestamp,
									'screenshot_url': url.screenshot_url})
		return render(request, 'urlexpander2/url_update_form.html', {'form': form})
	else:
		url = get_object_or_404(Url, pk=pk)
		url.shortened = request.POST['shortened']
		url.destination = request.POST['destination']
		url.status = request.POST['status']
		url.title = request.POST['title']
		url.snapshot_url = request.POST['snapshot_url']
		url.timestamp = request.POST['timestamp']
		url.screenshot_url = request.POST['screenshot_url']
		url.save()
		return redirect('urlexpander2:index')

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
def UrlDelete(request, pk):
	url = get_object_or_404(Url, pk=pk)
	url.delete()
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	mybucket = conn.get_bucket('lab3images')
	k = Key(mybucket)
	k.key = pk
	k.delete()
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

# <-------------REST API --------------->
@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
@api_view(['GET','POST'])
def rest_index(request, format=None):
	if request.method == 'GET':
		urls = Url.objects.all()
		serializer = UrlListSerializer(urls, many=True)
		return Response(serializer.data)
	elif request.method == 'POST':
		serializer = UrlDetailSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/urlexpander2/accounts/login/')
@api_view(['GET', 'DELETE'])
def rest_detail(request, pk, format=None):
	url = get_object_or_404(Url, pk=pk)
	if request.method == 'GET':
		serializer = UrlDetailSerializer(url)
		return Response(serializer.data)
	elif request.method == 'DELETE':
		url.delete()

@login_required(login_url='/urlexpander2/accounts/login/')
@api_view(['GET'])
def rest_update(request, pk, format=None):

    url = get_object_or_404(Url, pk=pk)

    #wayback
    arch_url = 'http://archive.org/wayback/available?url=' + url.shortened
    checked = requests.get(arch_url)
    data = json.loads(checked.text)
    snapshot = data['archived_snapshots']['closest']['url']
    timestamp = data['archived_snapshots']['closest']['timestamp']
    url.snapshot_url = snapshot
    url.timestamp = timestamp

    #phantomJS
    api_key = 'ak-cyywv-37en6-w9yr4-3df7w-7ygkz'
    response = '{url:"' + snapshot + '",renderType:"jpg",outputAsJson:false}'
    screenshot_url = 'http://PhantomJsCloud.com/api/browser/v2/' + api_key + '/?request=' + response
    url.screenshot_url = screenshot_url
    url.save()

    #S3
    resource = requests.get(screenshot_url)
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    mybucket = conn.get_bucket('lab3images')
    k = Key(mybucket)
    k.key = url.pk
    k.set_contents_from_string(resource.content)

    serializer = UrlDetailSerializer(url)
    return Response(serializer.data)
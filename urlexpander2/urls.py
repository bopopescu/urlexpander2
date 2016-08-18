"""urlexpander2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'urlexpander2'

urlpatterns = [

    #Auth
    url(r'^accounts/login/$', auth_views.login),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # /urlexpander2/
    url(r'^$', views.index, name='index'),
    # /urlexpander2/1234
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # /urlexpander2/add/
    url(r'^add/$', views.add_url, name = 'url-add'),
    # /urlexpander2/update/1234
    url(r'^update/(?P<pk>[0-9]+)$', views.UrlUpdate, name = 'url-update'),
    # /urlexpander2/delete/1234
    url(r'^delete/(?P<pk>[0-9]+)$', views.UrlDelete, name = 'url-delete'),

    #REST API
    url(r'^api/get/$', views.rest_index, name='api-index'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.rest_detail, name='api-detail'),
    url(r'^api/add/(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])/$', views.rest_add, name='api-add'),
]

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
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    # /urlexpander2/
    url(r'^$', views.IndexView.as_view(), name='index'),
    #/urlexpander2/register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # /urlexpander2/1234
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /urlexpander2/add/
    url(r'^add/$', views.add_url, name = 'url-add'),
    # /urlexpander2/update/1234
    url(r'^update/(?P<pk>[0-9]+)$', views.UrlUpdate.as_view(), name = 'url-update'),
    # /urlexpander2/delete/1234
    url(r'^delete/(?P<pk>[0-9]+)$', views.UrlDelete.as_view(), name = 'url-delete'),
]

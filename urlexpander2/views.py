from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from .models import Url
from .forms import UserForm
from django.http import HttpResponse
import requests, bs4

class IndexView(generic.ListView):
    template_name = 'urlexpander2/index.html'
    context_object_name = 'all_urls'

    def get_queryset(self):
        return Url.objects.all()

class DetailView(generic.DetailView):
    model = Url
    template_name = 'urlexpander2/detail.html'

def add_url(request):
    html = request.url
    return HttpResponse(html)
    #new_url = Url()
    #new_url.shortened = request.input

    #r = requests.get(request.data)

    #new_url.destination = url.url
    #new_url.status = url.status_code

    #beautiful = bs4.BeautifulSoup(url.text)
    #new_url.title = beautiful.title.text

    #new_url.save()
    #return redirect('urlexpander2/detail.html', new_url.pk)

class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'urlexpander2/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request,self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form})

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Url

class IndexView(generic.ListView):
    template_name = 'urlexpander2/index.html'
    context_object_name = 'all_urls'

    def get_queryset(self):
        return Url.objects.all()

class DetailView(generic.DetailView):
    model = Url
    template_name = 'urlexpander2/detail.html'

class UrlCreate(CreateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']


class UrlUpdate(UpdateView):
    model = Url
    fields = ['shortened', 'destination', 'status', 'title']

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('IndexView')


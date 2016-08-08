from django.views import generic
from .models import Url

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Url.objects.all()

class DetailView(generic.DetailView):
    model = Url
    template_name = 'detail.html'

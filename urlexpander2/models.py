from django.db import models
from django.core.urlresolvers import reverse
import requests, bs4

class Url(models.Model):
    shortened = models.URLField()
    r = requests.get(shortened)

    destination = models.URLField(r.url)
    status = models.IntegerField(r.status_code)

    title = models.CharField(bs4.BeautifulSoup(r.text).title.text, max_length=500)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

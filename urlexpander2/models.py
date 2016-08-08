from django.db import models
from django.core.urlresolvers import reverse
import requests, bs4

class Url(models.Model):
    shortened = models.URLField()
    r = requests.get(shortened)

    destination = models.URLField()
    destination = r.url

    status = models.IntegerField()
    status = r.status_code

    title = models.CharField(max_length=500)
    title = bs4.BeautifulSoup(r.text).title.text

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

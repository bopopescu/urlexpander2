from django.db import models
from django.core.urlresolvers import reverse
import requests, bs4

class Url(models.Model):
    shortened = models.URLField()
    r = requests.get(shortened)

    destination = r.url
    status = r.status_code

    beautiful = bs4.BeautifulSoup(r.text)
    title = beautiful.title.text

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

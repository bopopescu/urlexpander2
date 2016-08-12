from django.db import models
from django.core.urlresolvers import reverse


class Url(models.Model):
    shortened = models.URLField()
    destination = models.URLField()
    status = models.IntegerField()
    title = models.CharField(max_length=500)
    snapshot_url = models.CharField(max_length=1000, default='http://google.com')
    timestamp = models.CharField(max_length=15, default='1234567')

    #def get_absolute_url(self):
     #   return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)


from django.db import models
from django.core.urlresolvers import reverse

class Url(models.Model):
    shortened = models.URLField()
    destination = models.URLField()
    status = models.SmallIntegerField()
    title = models.CharField(max_length = 500)

    def get_absolute_url(self):
        return reverse('detail.html', kwargs={'pk': self.pk})

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

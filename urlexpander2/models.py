from django.db import models

class Url(models.Model):
    shortened = models.URLField()
    destination = models.URLField()
    status = models.SmallIntegerField()
    title = models.CharField(max_length = 500)

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

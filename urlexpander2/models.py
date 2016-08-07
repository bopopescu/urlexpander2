from django.db import models

class Url(models.Model):
    shortened = models.URLField()
    destination = models.URLField()
    status = models.SmallIntegerField()
    title = models.CharField(max_length = 500)
    is_favorite = models.BooleanField(default = False)

    def __str__(self):
        return 'Url ' + str(self.id) + ': ' + str(self.shortened)

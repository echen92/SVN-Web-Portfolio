from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

class Project(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "message"
        verbose_name_plural = "messages"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('message_detail', args=(self.pk,))

    class Admin:
        pass

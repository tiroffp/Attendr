from django.db import models
from django.core.urlresolvers import reverse


class Roll(models.Model):

    def get_absolute_url(self):
        return reverse('view_create_roll', args=[self.id])


class Attendee(models.Model):
    name = models.TextField(default='')
    roll = models.ForeignKey(Roll, default=None)
    order = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('roll', 'name')

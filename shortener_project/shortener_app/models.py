from django.db import models
from django.utils import timezone


class MyUrl(models.Model):
    real_url = models.URLField(max_length=500)
    created_by_id = models.PositiveIntegerField(default=0)
    short_url = models.SlugField(max_length=6, unique=True)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    used_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        return self.real_url

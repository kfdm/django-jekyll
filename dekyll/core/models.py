from django.db import models


class Post(models.Model):
    raw = models.TextField()
    date = models.DateField()
    dirty = models.BooleanField()
    slug = models.SlugField()

    class Meta:
        ordering = ('-date',)

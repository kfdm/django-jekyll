from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Post(models.Model):
    raw = models.TextField()
    frontmatter = models.TextField()
    date = models.DateField()
    dirty = models.BooleanField()
    slug = models.SlugField(unique=True)

    tag_set = GenericRelation('core.Tag')

    class Meta:
        ordering = ('-date',)


class Page(models.Model):
    raw = models.TextField()
    dirty = models.BooleanField()
    slug = models.SlugField()

    tag_set = GenericRelation('core.Tag')


class Tag(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag

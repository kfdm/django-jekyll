from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'dirty')


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'dirty')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    def _object_slug(self, object):
        return object.content_object.slug

    list_display = ('tag', '_object_slug')

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
    list_display = ('tag', 'content_object')

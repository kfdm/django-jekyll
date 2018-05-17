from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView

from dekyll.core import models


class PostListView(ListView):

    model = models.Post
    paginate_by = 100  # if pagination is desired

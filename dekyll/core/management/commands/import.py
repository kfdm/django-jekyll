import json
import os
import re

from django.core.management.base import BaseCommand

import yaml
from dekyll.core import models


class Importer(object):
    def __init__(self, path):
        self.path = path
        self.fn = os.path.basename(path)

        with open(path, encoding='utf8') as fp:
            raw_text = fp.read()
            in_frontmatter = None
            frontmatter = ''
            body = ''
            for line in raw_text.split('\n'):
                if in_frontmatter and line == '---':
                    in_frontmatter = False
                    continue
                if in_frontmatter is None and line == '---':
                    in_frontmatter = True
                    continue
                if in_frontmatter:
                    frontmatter += line + '\n'
                    continue
                body += line + '\n'
        self.body = body
        self.frontmatter = frontmatter


class Page(Importer):
    re_path = re.compile('(?P<page>.*)\.(?P<ext>md|markdown)')

    def process(self):
        print(self.path)
        return None, None


class Post(Importer):
    re_path = re.compile('(?P<year>\w{4})-(?P<month>\w{2})-(?P<day>\w{2})-(?P<slug>.*)\.(?P<ext>md|markdown)')
    model = models.Post

    def process(self):
        year, month, day, slug, ext = self.re_path.match(self.fn).groups()

        frontmatter = yaml.safe_load(self.frontmatter)
        frontmatter.setdefault('title', self.fn)
        # frontmatter.setdefault('date', '{}-{}-{}'.format(year, month, day))
        frontmatter['date'] = '{}-{}-{}'.format(year, month, day)
        frontmatter.setdefault('slug', slug)
        frontmatter.setdefault('tags', [])

        obj, created = self.model.objects.update_or_create(
            slug=frontmatter['slug'],
            defaults={
                'raw': self.body,
                'frontmatter': json.dumps(frontmatter),
                'date': frontmatter['date'],
                'dirty': False,
            }
        )
        for tag in frontmatter['tags']:
            obj.tag_set.create(tag=tag)
        return obj, created


class Command(BaseCommand):
    help = 'Reload Pages'
    re_path = re.compile('(?P<year>\w{4})-(?P<month>\w{2})-(?P<day>\w{2})-(?P<slug>.*)\.(?P<ext>md|markdown)')

    def add_arguments(self, parser):
        parser.add_argument('path', default='.')

    def handle(self, path, *args, **options):
        self.stderr.write('Setting objects as dirty')
        created = 0
        updated = 0
        deleted = 0

        Post.model.objects.update(dirty=True)

        for dirpath, dirnames, filenames in os.walk(path):

            # Prune out special directories like .git
            for prune in dirnames:
                if prune.startswith('.'):
                    dirnames.remove(prune)

            for fn in filenames:
                match = Post.re_path.match(fn)
                if match:
                    post, new_post = Post(os.path.join(dirpath, fn)).process()
                    if new_post:
                        created += 1
                    else:
                        updated += 1
                    continue
                match = Page.re_path.match(fn)
                if match:
                    page, new_page = Page(os.path.join(dirpath, fn)).process()


        print('Created', created)
        print('Updated', updated)
        print('Deleted', deleted)

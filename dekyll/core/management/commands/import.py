import os

from django.core.management.base import BaseCommand

import yaml
import re
from dekyll.core.models import Post


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

        Post.objects.update(dirty=True)

        for dirpath, dirnames, filenames in os.walk(path):

            # Prune out special directories like .git
            for prune in dirnames:
                if prune.startswith('.'):
                    dirnames.remove(prune)

            for fn in filenames:
                match = self.re_path.match(fn)
                if match is None:
                    continue
                year, month, day, slug, ext = match.groups()

                with open(os.path.join(dirpath, fn), encoding='utf8') as fp:
                    print(fp.name)

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

                frontmatter = yaml.safe_load(frontmatter)
                frontmatter.setdefault('title', fp.name)
                #frontmatter.setdefault('date', '{}-{}-{}'.format(year, month, day))
                frontmatter['date'] = '{}-{}-{}'.format(year, month, day)
                frontmatter.setdefault('slug', slug)

                post, new_post = Post.objects.update_or_create(
                    slug=frontmatter['slug'],
                    defaults={
                        'raw': body,
                        'date': frontmatter['date'],
                        'dirty': False,
                    }
                )
                if new_post:
                    created += 1
                else:
                    updated += 1

        print('Created', created)
        print('Updated', updated)
        print('Deleted', deleted)

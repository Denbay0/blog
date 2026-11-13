from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from blogs.models import BlogPost


class Command(BaseCommand):
    help = 'Create three distinct demonstration posts for an existing author.'

    def add_arguments(self, parser):
        parser.add_argument('--owner', help='Username of the author; defaults to the first existing user')

    def handle(self, *args, **options):
        users = get_user_model().objects
        owner = users.filter(username=options['owner']).first() if options['owner'] else users.order_by('pk').first()
        if owner is None:
            raise CommandError('Create a user or superuser before seeding the blog.')
        posts = [
            ('Первые шаги с Django', 'Создали проект, подключили приложение blogs и настроили маршруты.'),
            ('Модели и миграции', 'Публикации сохраняются в базе данных, а миграции обновляют схему без потери записей.'),
            ('Права автора', 'Читать публикации может каждый, а редактировать — только их автор.'),
        ]
        for title, body in posts:
            BlogPost.objects.get_or_create(title=title, owner=owner, defaults={'text': body})
        self.stdout.write(self.style.SUCCESS('Three demonstration posts are available in the admin.'))

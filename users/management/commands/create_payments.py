from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создаёт группу модераторов'

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name='moderators')
        self.stdout.write(self.style.SUCCESS("Группа 'moderators' создана или уже существует."))

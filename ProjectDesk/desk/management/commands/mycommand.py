from django.core.management.base import BaseCommand, CommandError
from ProjectDesk.desk.models import Post
class Command(BaseCommand):
    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return
        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано
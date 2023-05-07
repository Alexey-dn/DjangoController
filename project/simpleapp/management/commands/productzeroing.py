from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Product


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer != 'yes':  # в случае подтверждения действительно удаляем все товары
            self.stdout.write(self.style.ERROR(
                'Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано
        else:
            for product in Product.objects.all():
                product.quantity = 0
                product.save()
            self.stdout.write(self.style.SUCCESS('Successfully wiped products!'))
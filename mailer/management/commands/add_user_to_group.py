from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db.models import QuerySet


class Command(BaseCommand):
    help = 'Добавление пользователя в группу модераторов'

    # Группы и разрешения
    my_groups = {
        'moderator_mail': [
            'client.view_client_list',
            'mailer.view_mailingmessage',
            'mailer.change_mailingsettings',
            'mailer.view_mailingsettings',
            'users.change_user',
            'users.view_user',
        ],
        'moderator_blog': [
            'blog.view_post',
            'blog.change_post',
            'blog.delete_post',
            'blog.add_post',
        ]
    }

    def handle(self, *args, **options):

        # Создаем группы
        user_input = input('Создать группы [Y/n]:\n').lower()
        if user_input == 'y':
            self.create_groups(self.my_groups)
            print(f'Созданы группы: {", ".join(self.my_groups.keys())}')

        # Выбираем пользователя
        while True:
            try:
                user_input = int(input('Введите pk пользователя:\n'))
                user = self.get_user(user_input)
                if not user:
                    self.print_user(user)
                    continue
            except ValueError:
                print('Не корректный ввод, введите число')
                continue
            else:
                self.print_user(user)
                break

        # Выбираем группу
        all_groups = Group.objects.all()
        [print(i, v) for i, v in enumerate(all_groups)]
        while True:
            user_input = input('Выберите группу для пользователя:\n')
            try:
                index = int(user_input)
                group = self.get_group(all_groups, index)
            except ValueError:
                print('Не корректный ввод, введите число')
                continue
            except IndexError:
                print('Выберите правильный индекс группы')
                continue
            else:
                group.user_set.add(user)
                print(f'Пользователь {user} добавлен в группу {group}')
                break

    def create_groups(self, groups: dict) -> None:
        """ Создаем группы и привязываем разрешениям к ним """

        for group_name, permissions in groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for permission in permissions:
                content_type, codename = permission.split('.')
                permission, _ = Permission.objects.get_or_create(codename=codename)
                group.permissions.add(permission)

            group.save()

    def get_user(self, user_id: int) -> get_user_model() | None:
        """ Получаем пользователя по id """

        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

    def print_user(self, user):
        if user is None:
            print('Пользователь не найден')
        else:
            print(f'Пользователь выбран:\npk: {user.pk} email: {user.email} username: {user.username}')

    def get_group(self, groups: QuerySet, index: int) -> Group | ValueError:
        """ Получаем группу по индексу """

        if index > len(groups) or index < 0:
            raise ValueError('Не верный индекс группы')
        return groups[index]

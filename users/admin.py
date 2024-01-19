from django.contrib import admin
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['first_name', 'last_name', 'email']
    exclude = ['password']
    filter_horizontal = [
        'groups',
        'user_permissions',
    ]
    save_on_top = True
    fieldsets = (
        (
            _('Personal info'),
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """ Оставляю персоналу все поля для чтения кроме is_active что бы он мог блокировать пользователей """

        if not request.user.has_perm('users.can_view_all_fields'):
            active_fields = {
                'is_active',
            }
            readonly_fields = [field.name for field in self.model._meta.get_fields() if field.name not in active_fields]
            return readonly_fields
        return []

    def get_queryset(self, request):
        """ Для персонала исключил всех кроме пользователей, что бы они не могли банить друг друга """

        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False, is_staff=False)
        return queryset

    def get_object(self, request, object_id, from_field=None):
        """ Для персонала отключил возможность просматривать персонал прыгая по урлам в админке """

        obj = super().get_object(request, object_id, from_field)
        if not request.user.has_perm('can_view_is_staff'):
            if obj is None:
                raise Http404('Пользователь не существует')
            elif obj.is_staff or obj.is_superuser:
                raise Http404('Недостаточно прав для просмотра этого пользователя')
        return obj

from django.contrib import admin
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

        if not request.user.has_perm('can_view_all_fields'):
            readonly_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                               'groups', 'user_permissions', 'last_login', 'date_joined', 'is_staff', 'is_superuser')
            return readonly_fields
        return []

    def get_queryset(self, request):
        """ Для персонала исключил всех кроме пользователей, что бы они не могли банить друг друга """

        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False, is_staff=False)
        return queryset


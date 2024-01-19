from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from mailer.models import MailingSettings, MailingMessage, MailingLogger


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ['clients']
    list_display = ['title', 'is_active', 'owner', 'frequency', 'status']
    list_filter = ['is_active', 'owner', 'status']
    actions = ['make_active', 'make_inactive']

    @admin.action(description='Сделать рассылку активной')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Сделать рассылку неактивной')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def get_readonly_fields(self, request, obj=None):
        """ Оставляю персоналу все поля для чтения кроме is_active что бы он мог блокировать рассылки """

        if not request.user.has_perm('mailer.can_view_all_fields'):
            active_fields = {
                'is_active',
            }
            readonly_fields = [field.name for field in self.model._meta.get_fields() if field.name not in active_fields]
            self.fields = ['title', 'time_start', 'time_end', 'frequency', 'status', 'is_active', 'mail', 'owner']
            return readonly_fields
        return []


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'get_author',
    ]

    @admin.display(description='ссыль')
    def get_author(self, obj):
        # url = reverse('admin:auth_user_change', args=[obj.author.id])
        url = f'http://127.0.0.1:8000/admin/users/user/{obj.author.id}/change/'  # костыль потом поправлю
        return mark_safe(f'<a href="{url}">{obj.author}</a>')


@admin.register(MailingLogger)
class MailingLoggerAdmin(admin.ModelAdmin):
    pass

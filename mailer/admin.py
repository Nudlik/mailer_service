from django.contrib import admin

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
            return readonly_fields
        return []


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(MailingLogger)
class MailingLoggerAdmin(admin.ModelAdmin):
    pass

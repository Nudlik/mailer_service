from django.contrib import admin

from mailer.models import MailingSettings, MailingMessage, MailingLogger


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    filter_horizontal = ['clients']


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(MailingLogger)
class MailingLoggerAdmin(admin.ModelAdmin):
    pass

from datetime import datetime

from django.core.management import BaseCommand

from mailer.models import MailingSettings
from mailer.utils import check_day_dispatch, send_mail_custom


class Command(BaseCommand):
    help = 'Старт запуска рассылок'

    def handle(self, *args, **options):

        date_now = datetime.now().date()

        # переводим рассылки в активные
        created_mails = MailingSettings.objects.filter(
            is_active=True,
            status=MailingSettings.STATUS.CREATED,
            time_start__lte=date_now,
            time_end__gte=date_now,
        )
        for mail in created_mails:
            mail.status = MailingSettings.STATUS.ACTIVE
            mail.save()

        # выбираем рассылки для отправки писем
        mail_settings = MailingSettings.objects.filter(
            is_active=True,
            status=MailingSettings.STATUS.ACTIVE,
        )

        for mail_setting in mail_settings:
            time_start = mail_setting.time_start
            time_end = mail_setting.time_end
            frequency = mail_setting.frequency

            # логика отправки
            if time_start <= date_now <= time_end:
                if check_day_dispatch(date_now, time_start, time_end, frequency):
                    for client in mail_setting.clients.all():
                        send_mail_custom(mail_setting, client)

            # если рассылка закончилась переводим в неактивные
            if date_now >= time_end:
                mail_setting.status = MailingSettings.STATUS.INACTIVE

            mail_setting.save()

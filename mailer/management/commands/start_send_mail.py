from datetime import datetime

from django.core.management import BaseCommand

from mailer.models import MailingSettings
from mailer.utils import check_day_dispatch, send_mail_custom


class Command(BaseCommand):
    help = 'Старт запуска рассылок'

    def handle(self, *args, **options):

        date_now = datetime.now().date()

        mail_settings = MailingSettings.objects.filter(
            is_active=True,
            status=MailingSettings.STATUS.ACTIVE,
        )

        for mail_setting in mail_settings:
            time_start = mail_setting.time_start
            time_end = mail_setting.time_end
            frequency = mail_setting.frequency

            if time_start <= date_now <= time_end:
                if check_day_dispatch(date_now, time_start, time_end, frequency):
                    for client in mail_setting.clients.all():
                        send_mail_custom(
                                subject=mail_setting.mail.title,
                                message=mail_setting.mail.message,
                                from_email='my@my.ru',
                                recipient_list=[client.email]
                            )

            if date_now >= time_end:
                mail_setting.status = MailingSettings.STATUS.INACTIVE

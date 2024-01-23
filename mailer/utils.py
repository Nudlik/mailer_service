from datetime import timedelta, date
import smtplib

from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import QuerySet

from config import settings
from mailer.models import MailingSettings, MailingLogger


class MenuMixin:
    page_title: str = None
    page_description: str = None

    def get_mixin_context(self, context: dict, **kwargs) -> dict:
        context.update(kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.page_title is not None:
            context['title'] = self.page_title

        if self.page_description is not None:
            context['description'] = self.page_description

        return context


def check_day_dispatch(now_date: date, start_date: date, end_date: date, frequency: str) -> bool:
    """ Проверка даты отправки рассылки """

    if now_date < start_date or now_date > end_date:
        return False
    elif frequency == 'daily':
        return True

    current_date, flag = start_date, False
    delta_dict = {
        'weekly': timedelta(weeks=1),
        'monthly': relativedelta(months=+1)
    }
    frequency = delta_dict[frequency]
    while current_date <= end_date:
        if current_date == now_date:
            flag = True
            break
        current_date += frequency

    return flag


def send_mail_custom(mail_setting: MailingSettings, client: MailingSettings.clients) -> None:
    """ Отправка письма каждому клиенту(что получатель не видел список отправителям) с логированием """

    mail = mail_setting.mail

    status = MailingLogger.STATUS.SUCCESS
    error_msg = None
    try:
        send_mail(
            subject=mail.title,
            message=mail.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client],
        )
    except smtplib.SMTPException as e:
        error_msg = e
        status = MailingLogger.STATUS.ERROR
    except Exception as e:
        error_msg = e
        status = MailingLogger.STATUS.ERROR
    finally:
        log = MailingLogger.objects.create(
            status=status,
            error=error_msg,
            setting=mail_setting,
        )
        log.save()


def cache_for_queryset(key: str, queryset: QuerySet, time: int = settings.CACHE_TIMEOUT) -> QuerySet:
    """ Кеширует queryset запрос к базе данных """

    if not settings.CACHES_ENABLED:
        return queryset
    queryset_cache = cache.get(key)
    if queryset_cache is not None:
        return queryset_cache
    cache.set(key, queryset, time)
    return queryset

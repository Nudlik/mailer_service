import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger('apscheduler')
logger.setLevel(logging.DEBUG)


def run_mailing():
    call_command('start_send_mail')


def my_job():
    logger.info('Hello World!')


# Декоратор `close_old_connections` гарантирует, что соединения с базой данных, которые стали непригодны
# для использования или устарели, закрываются до и после выполнения вашего задания. Вы должны использовать это
# для обертывания любых запланированных вами заданий, которые каким-либо образом обращаются к базе данных Django.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет из базы данных записи выполнения заданий APScheduler старше max_age.
    Это помогает предотвратить заполнение базы данных старыми историческими записями, которые не являются
    дольше полезно.

    :param max_age: Максимальный срок хранения исторических записей выполнения заданий.
                    По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Запуск APScheduler.'

    def add_arguments(self, parser):
        parser.add_argument('-b', '--background', action='store_true', help='Запустить в фоновом режиме')
        parser.add_argument('-s', '--stop', action='store_true', help='Остановить работу APScheduler')

    def handle(self, *args, **options):
        background = options.get('background', False)
        stop = options.get('stop', False)

        scheduler = self.start_apscheduler(background)
        if stop:
            self.stop_apscheduler(scheduler)
            return

        # добавляем таблицу в jobstore
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        # добавляем задание с отправкой писем
        scheduler.add_job(
            run_mailing,
            trigger=CronTrigger(hour='01', minute='00'),
            id='run_mailing',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added job "run_mailing".')

        # дебажная запись в логи для проверки работы
        debag = False
        if debag:
            scheduler.add_job(
                my_job, trigger=CronTrigger(second='*/10'), id='my_job', max_instances=1, replace_existing=True
            )
            logger.info('Added job "my_job".')

        # добавляем задание на удаление старых записей в таблице
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),  # Полночь понедельника, перед началом следующей рабочей недели.
            id='delete_old_job_executions',
            max_instances=1,
            replace_existing=True,
        )
        logger.info('Added weekly job: "delete_old_job_executions".')

        try:
            logger.info('Starting scheduler...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down successfully!')

    @staticmethod
    def stop_apscheduler(scheduler: BackgroundScheduler | BlockingScheduler) -> None:
        """ Остановить работу APScheduler """

        try:
            logger.info('Stopping scheduler...')
            scheduler.shutdown()
            logger.info('Scheduler shut down!')
        except Exception as e:
            logger.error(e)

    @staticmethod
    def start_apscheduler(background: bool) -> BackgroundScheduler | BlockingScheduler:
        """ Запустить работу APScheduler """

        if background:
            return BackgroundScheduler(timezone=settings.TIME_ZONE)
        return BlockingScheduler(timezone=settings.TIME_ZONE)

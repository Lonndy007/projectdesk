import logging
import datetime
from django.conf import settings
from ProjectDesk.desk.models import Post,Category
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time__gte=last_week)
    categoriest = set(posts.values_list('post_category',flat=True))
    subscribers = set(Category.objects.filter(name_of_category__in=categoriest).values_list('subscribers',flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link':settings.SITE_URL,
            'posts':posts
        }
    )
    msg = EmailMultiAlternatives(subject='Статьи за неделю',body='',from_email=settings.EMAIL_HOST_USER,to=subscribers)
    msg.attach_alternative(html_content,'text/html')
    msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='wen',hour=20,minute='48'),
        id = 'my_job' ,
        max_instances = 1,
        replace_existing = True),
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

class Command(BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()
        if answer == 'yes':
            Post.objects.all().delete
            self.stdout.write(self.style.SUCCESS('Succesfully wiped products!'))
            return
        self.stdout.write(self.style.ERROR('Access denied'))


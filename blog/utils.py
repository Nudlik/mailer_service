from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse

from config.settings import env


def send_mail_custom(request, obj):
    site = get_current_site(request)
    post_url = reverse('blog:post_detail', args=[obj.slug])
    absolute_url = f'{request.scheme}://{site.domain}{post_url}'
    send_mail(
        subject=f'Пост "{obj.title}" набрал 100 просмотров',
        message=f'Поздравляю и тд и тп... перейдите по ссылке для просмотра {absolute_url}',
        from_email=env.str('EMAIL_HOST_USER'),
        recipient_list=[env.str('EMAIL_HOST_USER')],
        fail_silently=False,
    )

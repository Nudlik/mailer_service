from django.urls import path, include

from mailer import apps
from mailer.views import IndexTemplateView

app_name = apps.MailerConfig.name

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='home'),
]

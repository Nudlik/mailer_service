from django.views.generic import TemplateView

from blog.models import Post
from mailer.models import MailingSettings
from mailer.utils import MenuMixin


class IndexTemplateView(MenuMixin, TemplateView):
    template_name = 'mailer/index.html'
    page_title = 'Главная страница'
    page_description = 'Сайт где вы можете создавать запланированные рассылки клиентам'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            total_count=MailingSettings.objects.count(),
            total_active=MailingSettings.objects.filter(status=MailingSettings.STATUS.ACTIVE).count(),
            total_client=MailingSettings.objects.filter(clients__isnull=False).distinct().count(),
            random_post=Post.objects.order_by('?')[:3],
        )

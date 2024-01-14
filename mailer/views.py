from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = 'mailer/index.html'
    page_title = 'Главная страница'

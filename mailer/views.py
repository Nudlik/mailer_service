from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView

from mailer.forms import MessageForm, SettingsForm
from mailer.models import MailingMessage, MailingLogger, MailingSettings
from mailer.utils import MenuMixin


class IndexTemplateView(MenuMixin, TemplateView):
    template_name = 'mailer/index.html'
    page_title = 'Главная страница'
    page_description = 'Сайт где вы можете создавать запланируемые рассылки клиентам'


class SendView(TemplateView):
    template_name = 'mailer/send.html'


# --------------------------------- MailingMessage ---------------------------------------------
class MessageListView(MenuMixin, ListView):
    model = MailingMessage
    paginate_by = 3
    page_title = 'Список всех писем'
    page_description = 'Здесь отображены все письма созданные вами'


class MessageDetailView(MenuMixin, DetailView):
    model = MailingMessage
    page_description = 'Здесь можно просмотреть содержимое письма'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра письма "{self.object.title}"',
        )


class MessageCreateView(MenuMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    page_title = 'Страница создания письма'
    page_description = 'Здесь можно создать новое письмо'

    def get_success_url(self):
        return reverse_lazy('mailer:message_detail', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class MessageUpdateView(MenuMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    template_name = 'mailer/mailingmessage_form.html'
    page_title = 'Страница редактирования письма'
    page_description = 'Здесь можно редактировать письмо'


class MessageDeleteView(MenuMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailer:message_list')
    page_title = 'Страница удаления письма'
    page_description = 'Здесь можно удалить письмо'


# --------------------------------- MailingLogger ---------------------------------------------


# --------------------------------- MailingSettings -------------------------------------------

class SettingsListView(MenuMixin, ListView):
    model = MailingSettings
    paginate_by = 3
    page_title = 'Список всех рассылок'
    page_description = 'Здесь отображены все рассылки созданные вами'


class SettingsDetailView(MenuMixin, DetailView):
    model = MailingSettings
    page_description = 'Здесь можно просмотреть содержимое рассылки'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра рассылки "{self.object.title}"',
        )


class SettingsCreateView(MenuMixin, CreateView):
    model = MailingSettings
    form_class = SettingsForm
    page_title = 'Страница создания рассылки'
    page_description = 'Здесь можно создать настройки рассылки'

    def get_success_url(self):
        return reverse_lazy('mailer:settings_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SettingsUpdateView(MenuMixin, UpdateView):
    model = MailingSettings
    form_class = SettingsForm
    template_name = 'mailer/mailingsettings_form.html'
    page_title = 'Страница редактирования рассылки'
    page_description = 'Здесь можно изменить настройки рассылки'


class SettingsDeleteView(MenuMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailer:settings_list')
    page_title = 'Страница удаления рассылки'
    page_description = 'Здесь можно удалить рассылку'



from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView

from blog.models import Post
from mailer.forms import MessageForm, SettingsForm
from mailer.models import MailingMessage, MailingLogger, MailingSettings
from mailer.utils import MenuMixin


class IndexTemplateView(MenuMixin, TemplateView):
    template_name = 'mailer/index.html'
    page_title = 'Главная страница'
    page_description = 'Сайт где вы можете создавать запланируемые рассылки клиентам'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            mailing=MailingSettings.objects.aggregate(
                total_count=Count('pk'),
                total_active=Count('pk', filter=Q(status=MailingSettings.STATUS.ACTIVE)),
                total_client=Count('clients', distinct=True),
            ),
            random_post=Post.objects.order_by('?')[:3],
        )


class SendView(TemplateView):
    template_name = 'mailer/send.html'


# --------------------------------- MailingMessage ---------------------------------------------
class MessageListView(LoginRequiredMixin, MenuMixin, ListView):
    model = MailingMessage
    paginate_by = 3
    page_title = 'Список всех писем'
    page_description = 'Здесь отображены все письма созданные вами'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class MessageDetailView(LoginRequiredMixin, MenuMixin, DetailView):
    model = MailingMessage
    page_description = 'Здесь можно просмотреть содержимое письма'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра письма "{self.object.title}"',
        )

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'], author=self.request.user)


class MessageCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    page_title = 'Страница создания письма'
    page_description = 'Здесь можно создать новое письмо'

    def get_success_url(self):
        return reverse_lazy('mailer:message_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    template_name = 'mailer/mailingmessage_form.html'
    page_title = 'Страница редактирования письма'
    page_description = 'Здесь можно редактировать письмо'


class MessageDeleteView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailer:message_list')
    page_title = 'Страница удаления письма'
    page_description = 'Здесь можно удалить письмо'


# --------------------------------- MailingLogger ---------------------------------------------


# --------------------------------- MailingSettings -------------------------------------------

class SettingsListView(LoginRequiredMixin, MenuMixin, ListView):
    model = MailingSettings
    paginate_by = 3
    page_title = 'Список всех рассылок'
    page_description = 'Здесь отображены все рассылки созданные вами'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class SettingsDetailView(LoginRequiredMixin, MenuMixin, DetailView):
    model = MailingSettings
    page_description = 'Здесь можно просмотреть содержимое рассылки'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра рассылки "{self.object.title}"',
        )

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'], owner=self.request.user)


class SettingsCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    model = MailingSettings
    form_class = SettingsForm
    page_title = 'Страница создания рассылки'
    page_description = 'Здесь можно создать настройки рассылки'

    def get_success_url(self):
        return reverse_lazy('mailer:settings_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SettingsUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = MailingSettings
    form_class = SettingsForm
    template_name = 'mailer/mailingsettings_form.html'
    page_title = 'Страница редактирования рассылки'
    page_description = 'Здесь можно изменить настройки рассылки'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SettingsDeleteView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailer:settings_list')
    page_title = 'Страница удаления рассылки'
    page_description = 'Здесь можно удалить рассылку'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from mailer.forms import MessageForm
from mailer.models import MailingMessage
from mailer.utils import MenuMixin


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

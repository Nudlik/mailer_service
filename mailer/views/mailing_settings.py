from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from mailer.forms import SettingsForm
from mailer.models import MailingSettings
from mailer.utils import MenuMixin


class SettingsListView(LoginRequiredMixin, MenuMixin, ListView):
    model = MailingSettings
    paginate_by = 3
    page_title = 'Список всех рассылок'
    page_description = 'Здесь отображены все рассылки созданные вами'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user, is_active=True)


class SettingsDetailView(LoginRequiredMixin, MenuMixin, DetailView):
    model = MailingSettings
    page_description = 'Здесь можно просмотреть содержимое рассылки'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра рассылки "{self.object.title}"',
        )

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'], owner=self.request.user, is_active=True)


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

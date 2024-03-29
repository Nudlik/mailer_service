from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.forms import ClientForm
from client.models import Client
from mailer.utils import MenuMixin


class ClientListView(LoginRequiredMixin, MenuMixin, ListView):
    model = Client
    paginate_by = 3
    page_title = 'Список всех клиентов'
    page_description = 'Здесь отображены все клиенты добавленные вами'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, MenuMixin, DetailView):
    model = Client
    page_description = 'Здесь можно просмотреть информацию о клиенте'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра клиента "{self.object.fullname}"',
        )

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'], owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    model = Client
    form_class = ClientForm
    page_title = 'Страница создания клиента'
    page_description = 'Здесь можно создать нового клиента'

    def get_success_url(self):
        return reverse_lazy('client:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, MenuMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    page_title = 'Страница редактирования клиента'
    page_description = 'Здесь можно редактировать информацию о клиенте'


class ClientDeleteView(LoginRequiredMixin, MenuMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    page_title = 'Страница удаления клиента'
    page_description = 'Здесь можно удалить клиента'

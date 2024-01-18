from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.forms import ClientForm
from client.models import Client
from mailer.utils import MenuMixin


class ClientListView(MenuMixin, ListView):
    model = Client
    paginate_by = 3
    page_title = 'Список всех клиентов'
    page_description = 'Здесь отображены все клиенты добавленные вами'


class ClientDetailView(MenuMixin, DetailView):
    model = Client
    page_description = 'Здесь можно просмотреть информацию о клиенте'

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            context=super().get_context_data(**kwargs),
            title=f'Страница просмотра клиента "{self.object.fullname}"',
        )


class ClientCreateView(MenuMixin, CreateView):
    model = Client
    form_class = ClientForm
    page_title = 'Страница создания клиента'
    page_description = 'Здесь можно создать нового клиента'

    def get_success_url(self):
        return reverse_lazy('client:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(MenuMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    page_title = 'Страница редактирования клиента'
    page_description = 'Здесь можно редактировать информацию о клиенте'


class ClientDeleteView(MenuMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    page_title = 'Страница удаления клиента'
    page_description = 'Здесь можно удалить клиента'

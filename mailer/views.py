from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView

from mailer.forms import MessageForm
from mailer.models import MailingMessage, MailingLogger, MailingSettings


class IndexTemplateView(TemplateView):
    template_name = 'mailer/index.html'
    page_title = 'Главная страница'


class SendView(TemplateView):
    template_name = 'mailer/send.html'


# --------------------------------- MailingMessage ---------------------------------------------
class MessageListView(ListView):
    model = MailingMessage
    paginate_by = 3


class MessageDetailView(DetailView):
    model = MailingMessage


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy('mailer:message_detail', kwargs={'pk': self.object.pk})

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MessageForm
    template_name = 'mailer/mailingmessage_form.html'


class MessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailer:message_list')


# --------------------------------- MailingLogger ---------------------------------------------


# --------------------------------- MailingSettings -------------------------------------------


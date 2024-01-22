from django import forms

from client.models import Client
from mailer.models import MailingMessage, MailingSettings


class MessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }


class SettingsForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('draft', 'черновик'),
        ('created', 'создана'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=user)
        self.fields['mail'].queryset = MailingMessage.objects.filter(author=user)

    class Meta:
        model = MailingSettings
        fields = ['title', 'time_start', 'time_end', 'frequency', 'status', 'mail', 'clients']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time_start': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'time_end': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'mail': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

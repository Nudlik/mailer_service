from django import forms

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
    class Meta:
        model = MailingSettings
        fields = ['title', 'time_start', 'time_end', 'frequency', 'status', 'mail', 'clients']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time_start': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'time_end': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'mail': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

from django import forms

from mailer.models import MailingMessage


class MessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

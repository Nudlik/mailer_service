from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class WidgetsMixin:
    class Meta:
        widgets = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.Meta, 'widgets'):
            widgets = self.Meta.widgets
            if widgets:
                for field_name, widget in widgets.items():
                    self.fields[field_name].widget = widget


class LabelsMixin:
    class Meta:
        labels = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.Meta, 'labels'):
            labels = self.Meta.labels
            if labels:
                for field_name, label in labels.items():
                    self.fields[field_name].label = label


class UserLoginForm(WidgetsMixin, LabelsMixin, AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
        }
        labels = {
            'username': 'Логин / E-mail',
        }

    def clean(self):
        email = self.cleaned_data.get('username')  # or self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password is not None:
            self.user_cache = authenticate(self.request, email=email, password=password)

            if self.user_cache is None or not self.user_cache.email_verify:
                raise ValidationError('Электронная почта не подтверждена, проверьте свою электронную почту',
                                      code='invalid_login')

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserRegisterForm(WidgetsMixin, UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ваш пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
        }
        labels = {
            'username': 'Логин',
        }


class UserProfileUpdateForm(LabelsMixin, WidgetsMixin, forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
        }
        labels = {
            'username': 'Логин',
        }


class UserPasswordChangeForm(WidgetsMixin, PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль')
    new_password1 = forms.CharField(label='Новый пароль')
    new_password2 = forms.CharField(label='Подтверждение пароля')

    class Meta:
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserPasswordResetForm(WidgetsMixin, PasswordResetForm):
    class Meta:
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
        }


class UserSetPasswordForm(WidgetsMixin, SetPasswordForm):
    class Meta:
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

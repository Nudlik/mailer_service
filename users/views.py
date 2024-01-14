from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, DetailView, FormView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm, UserProfileForm, UserPasswordChangeForm, \
    UserPasswordResetForm, UserSetPasswordForm
from users.utils import send_email_for_verify


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {
        'title': 'Авторизация',
        'button': 'Войти',
    }


class UserLogoutView(LogoutView):
    pass


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    model = get_user_model()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user:confirm_email')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['button'] = 'Зарегистрироваться'
        return context

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        if not user.email_verify:
            send_email_for_verify(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой профиль'

        attrs = [('username', 'Никнейм'), ('email', 'Почта'), ('first_name', 'Имя'),
                 ('last_name', 'Фамилия'), ('phone', 'Телефон'), ('country', 'Страна')]
        items = context['user']
        profile = {attrs[i][1]: getattr(items, attrs[i][0]) for i in range(len(attrs)) if hasattr(items, attrs[i][0])}
        context['profile'] = profile

        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateForm
    extra_context = {
        'title': 'Редактирование профиля',
        'button': 'Сохранить',
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {
        'title': 'Смена пароля',
        'button': 'Сохранить',
    }


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    extra_context = {
        'title': 'Ваш пароль был успешно изменен!',
        'button': 'Вернуться в профиль',
    }


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = UserPasswordResetForm
    extra_context = {
        'title': 'Восстановление пароля',
        'button': 'Сбросить по E-mail',
    }


class UserPasswordResetDoneView(PasswordResetView):
    template_name = 'users/password_reset_done.html'
    extra_context = {
        'title': 'Сброс пароля',
    }


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = UserSetPasswordForm
    extra_context = {
        'title': 'Новый пароль',
        'button': 'Сохранить',
    }


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    extra_context = {
        'title': 'Восстановление пароля завершено',
    }


class EmailVerify(View):
    template_name = 'users/verify_email.html'

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('mailer:home')
        elif request.user.is_authenticated:
            return redirect('mailer:home')

        return redirect('user:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist, ValidationError):
            user = None
        return user


class UserVerifyResendView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/verify_email.html'
    success_url = reverse_lazy('users:confirm_email')
    form_class = UserPasswordResetForm
    extra_context = {
        'title': 'Повторная отправка верефикации на E-mail',
        'button': 'Отправить',
    }

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email, email_verify=False)
        if user.exists():
            return super().form_valid(form)
        return redirect('user:confirm_email')  # тут нужно подумать, в плане безопасности использования invalid_verify
        # или сделать огранниченое количество попыток на данных функционал

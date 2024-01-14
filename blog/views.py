import transliterate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from config.settings import env


class PostListView(ListView):
    model = Post
    page_title = 'Список статей'
    page_description = 'Здесь можно посмотреть все статьи'
    paginate_by = 3

    def get_queryset(self):
        return self.model.published.all()


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=['view_count'])

        if obj.view_count == 100:
            site = get_current_site(self.request)
            post_url = reverse('blog:post_detail', args=[obj.slug])
            absolute_url = f'{self.request.scheme}://{site.domain}{post_url}'
            send_mail(
                subject=f'Пост "{obj.title}" набрал 100 просмотров',
                message=f'Поздравляю и тд и тп... перейдите по ссылке для просмотра {absolute_url}',
                from_email=env.str('EMAIL_HOST_USER'),
                recipient_list=[env.str('EMAIL_HOST_USER')],
                fail_silently=False,
            )

        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для создания статьи'

    def form_valid(self, form):
        slug = transliterate.slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=slug).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для редактирования статьи'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug'])

    def test_func(self):
        check_perms = bool(
            self.get_object().author == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['blog.change_post'])
        )
        return check_perms


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    page_title = 'Страницы для удаление статьи'

    def test_func(self):
        check_perms = bool(
            self.get_object().author == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['blog.delete_post'])
        )
        return check_perms

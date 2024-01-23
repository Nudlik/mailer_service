import transliterate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from blog.utils import send_mail_custom
from mailer.utils import MenuMixin, cache_for_queryset
from config import settings


class PostListView(MenuMixin, ListView):
    model = Post
    page_title = 'Список статей'
    page_description = 'Здесь можно посмотреть все статьи'
    paginate_by = 3

    def get_queryset(self):
        queryset = cache_for_queryset(
            key=settings.CACHE_POST_LIST,
            queryset=self.model.published.all().select_related('author')
        )
        return queryset


class PostDetailView(MenuMixin, DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=['view_count'])

        if obj.view_count == 100:
            send_mail_custom(self.request, obj)

        return obj


class PostCreateView(LoginRequiredMixin, MenuMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для создания статьи'

    def get_success_url(self):
        cache.delete(settings.CACHE_POST_LIST)
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        slug = transliterate.slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=slug).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, MenuMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для редактирования статьи'

    def get_success_url(self):
        cache.delete(settings.CACHE_POST_LIST)
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug'])

    def test_func(self):
        check_perms = bool(
            self.get_object().author == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['blog.change_post'])
        )
        return check_perms


class PostDeleteView(UserPassesTestMixin, MenuMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    page_title = 'Страницы для удаление статьи'

    def get_success_url(self):
        cache.delete(settings.CACHE_POST_LIST)
        return reverse('blog:post_list')

    def test_func(self):
        check_perms = bool(
            self.get_object().author == self.request.user
            or self.request.user.is_superuser
            or self.request.user.has_perms(['blog.delete_post'])
        )
        return check_perms

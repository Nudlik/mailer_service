import transliterate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import PostForm
from blog.models import Post
from mailer.utils import MenuMixin


class PostListView(MenuMixin, ListView):
    model = Post
    page_title = 'Список статей'
    page_description = 'Здесь можно посмотреть все статьи'
    paginate_by = 3

    def get_queryset(self):
        return self.model.published.all()


class PostDetailView(MenuMixin, DetailView):
    model = Post
    page_title = 'Страница просмотра статьи'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj


class PostCreateView(PermissionRequiredMixin, MenuMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для создания статьи'
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        slug = transliterate.slugify(form.cleaned_data['title'])
        if self.model.objects.filter(slug=slug).exists():
            form.add_error('title', 'Пост с таким slug уже существует')
            return self.form_invalid(form=form)

        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, MenuMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form.html'
    page_title = 'Страница для редактирования статьи'
    permission_required = 'blog.change_post'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['slug'])


class PostDeleteView(PermissionRequiredMixin, MenuMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    page_title = 'Страницы для удаление статьи'
    permission_required = 'blog.delete_post'

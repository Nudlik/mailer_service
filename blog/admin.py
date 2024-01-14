from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'time_create', 'time_update', 'is_published']
    list_display_links = ['title']
    search_fields = ['title', 'content']
    list_filter = ['is_published', 'time_update']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']

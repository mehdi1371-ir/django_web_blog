from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified',)
    list_filter = ('title', 'author', 'status', 'datetime_modified',)
    ordering = ('-datetime_modified',)

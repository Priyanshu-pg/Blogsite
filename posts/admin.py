from django.contrib import admin

# Register your models here.

from .models import Post

# class PostAdmin(admin.ModelAdmin):
    # list_display = ('title', 'create_time', 'update_time')
    # list_display_links = ('title', 'create_time', 'update_time')
    # prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post)
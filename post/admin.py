from dataclasses import field
from django.contrib import admin
from post.models import Posts, Likes


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = tuple(map(lambda field: field.name, Posts._meta.local_fields))

admin.site.register(Likes)

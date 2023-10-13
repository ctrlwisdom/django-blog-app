from django.contrib import admin
from .models import Post, Category, User, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
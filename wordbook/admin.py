from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NoteBook, Post


admin.site.register(User)
admin.site.register(NoteBook)
admin.site.register(Post)
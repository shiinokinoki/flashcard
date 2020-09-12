from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, NoteBook, Post


admin.site.register(CustomUser)
admin.site.register(NoteBook)
admin.site.register(Post)

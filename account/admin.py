from django.contrib import admin
from blog.models import BlogModel
from .models import User
from django.contrib.auth.admin import UserAdmin


UserAdmin.list_display=['username','email','is_active']

admin.site.register(User,UserAdmin)

from django.contrib import admin
from django.urls import path, include
from .models import Review

# Register your models here.
path('admin/', admin.site.urls),
admin.site.register(Review)

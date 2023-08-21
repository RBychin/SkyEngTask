from django.contrib import admin
from .models import File, LogFile


# Register your models here.
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(LogFile)
class LogFileAdmin(admin.ModelAdmin):
    list_display = ['log']
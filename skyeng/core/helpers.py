import os

from django.core.files.storage import default_storage
from django.core.mail import send_mail

from core.models import LogFile


def create_log_file(file, msg):
    LogFile.objects.create(
        file=file,
        log=msg
    )


def delete_file(file):
    old_file_path = os.path.join(file.file.name)
    if default_storage.exists(old_file_path):
        default_storage.delete(old_file_path)

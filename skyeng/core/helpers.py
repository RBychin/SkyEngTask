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


def send_email_notification(obj):
    nl = '\n'
    message = (
        f'{obj.name} checks results.',
        (f'We have checked your file {obj.name}.\n\n'
         f'Result of checking the file for errors: '
         f'{obj.check_status} '
         f'{"-", len(obj.pep) if obj.pep else ""}\n'
         f'{nl.join([error for error in obj.pep]) if obj.pep else ""}'),
        'SkyEng@mail.ru',
        [obj.user.email]
    )
    send_mail(*message, fail_silently=False)
    obj.email_notification = True
    obj.save()

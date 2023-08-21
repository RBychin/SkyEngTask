import pycodestyle
from celery import shared_task
from django.core.mail import send_mail

from core.helpers import create_log_file
from core.models import File


@shared_task
def send_email_notification(obj):
    nl = '\n'
    message = (
        f'{obj.name} checks results.',
        (f'We have checked your file {obj.name}.\n\n'
         f'Result of checking the file for errors: '
         f'{obj.check_status} '
         f'{len(obj.pep) if obj.pep else ""}\n'
         f'{nl.join([error for error in obj.pep]) if obj.pep else ""}'),
        'SkyEng@mail.ru',
        [obj.user.email]
    )
    send_mail(*message, fail_silently=False)
    obj.email_notification = True
    obj.save()


@shared_task
def run_pep8_check():
    """Checks the code for PEP8 errors"""

    objs = File.objects.filter(is_new=True)
    for obj in objs:
        style = pycodestyle.StyleGuide()
        result = style.check_files([obj.file.path])
        obj.pep = result.get_statistics()
        if obj.pep:
            obj.check_status = 'Errors'
            create_log_file(obj, (
                f'errors found in {obj.name}: {len(result.get_statistics())}')
                            )
        else:
            obj.check_status = 'OK'
            create_log_file(obj, f'no errors found in {obj.name}')
        obj.is_new = False
        obj.save()
        send_email_notification(obj)

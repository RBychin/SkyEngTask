import pycodestyle
from celery import shared_task
from django.core.mail import send_mail

from core.helpers import create_log_file, send_email_notification
from core.models import File


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

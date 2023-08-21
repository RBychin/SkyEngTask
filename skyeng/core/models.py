import json
import os

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()

STATUS = [
    ('OK', 'OK'),
    ('Errors', 'Errors'),
    ('Waiting', 'Waiting')
]


class File(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='file name'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='files',
        verbose_name='file owner'
    )
    file = models.FileField(
        upload_to='media/',
    )
    is_new = models.BooleanField(
        default=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    check_status = models.CharField(
        max_length=10,
        choices=STATUS, default='Waiting',
        verbose_name='checking status'
    )
    email_notification = models.BooleanField(
        default=False,
        verbose_name='been sent'
    )
    pep = ArrayField(models.CharField(
        max_length=256,
        null=True,
        blank=True
    ),
        null=True,
        blank=True,
        verbose_name='PEP8 errors')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return os.path.basename(self.file.name)


class LogFile(models.Model):
    file = models.ForeignKey(
        File, on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='file'
    )
    log = models.CharField(
        max_length=100000,
        verbose_name='log text'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.log[:50]

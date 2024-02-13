from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    """Расширенная модель ползьзователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    position = models.CharField(max_length=25, verbose_name='должность')
    birthday = models.DateField(verbose_name='birthdate')
    tel = models.CharField(max_length=16)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}'

    class Meta:

        db_table = 'profile'
        verbose_name = 'cотрудник'
        verbose_name_plural = 'сотрудники'
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_language = models.ForeignKey("dictionary.Language", on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.default_language.name if self.default_language else " " }'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

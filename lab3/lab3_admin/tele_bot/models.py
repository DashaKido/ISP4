from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID пользователя в соц сети',
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Deadline(models.Model):
    profile = models.ForeignKey(
        to='tele_bot.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    EASY = 'E'
    NORMAL = 'N'
    HARD = 'H'
    choices = (
        (EASY, 'Easy'),
        (NORMAL, 'Normal'),
        (HARD, 'Hard'),
    )
    difficulty = models.CharField(
        verbose_name='Сложность',
        max_length=1,
        choices=choices,
        default=EASY,
    )
    task = models.TextField(
        verbose_name='Задача',
    )

    def __str__(self):
        return f'Дедлайн {self.pk} от {self.profile}'

    def is_upperclass(self):
        return self.difficulty in (self.EASY, self.HARD)

    class Meta:
        verbose_name = 'Дедлайн'
        verbose_name_plural = 'Дедлайны'

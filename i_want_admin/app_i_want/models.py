from django.db import models


class Profile(models.Model):
    user_id = models.BigIntegerField(verbose_name='id пользователя')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    role = models.CharField(max_length=20, verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Task(models.Model):
    CHOICE_CATEGORY = [
        ('Маркетинг', 'Маркетинг'),
        ('Дизайн', 'Дизайн'),
        ('Простая помощь', 'Простая помощь'),
        ('Копирайтинг', 'Копирайтинг'),
        ('Программирование', 'Программирование'),
        ('Аудио/Видео монтаж', 'Аудио/Видео монтаж'),
        ('Другое', 'Другое')
    ]

    CHOICE_STATUS = [
        ('Активный', 'Активный'),
        ('Не активный', 'Не активный'),
    ]

    user_id = models.BigIntegerField(verbose_name='id пользователя')
    title = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Стоимость')
    category = models.CharField(max_length=20, choices=CHOICE_CATEGORY, blank=True, default='Другое', verbose_name='Категория')
    status = models.CharField(max_length=20, choices=CHOICE_STATUS, default='Активный', verbose_name='Статус')

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['-status']


class TaskResp(models.Model):
    user_id = models.BigIntegerField(verbose_name='id пользователя')
    username = models.CharField(max_length=50, verbose_name='Имя пользователя')
    task_id = models.IntegerField(verbose_name='id задания')
    resp_text = models.TextField(verbose_name='Отклик')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class BotMessage(models.Model):
    chat = models.BigIntegerField(verbose_name='id чата')
    message = models.BigIntegerField(blank=True, default = 0, verbose_name='id сообщения')

    class Meta:
        verbose_name = 'Сообщение бота'
        verbose_name_plural = 'Сообщения бота'

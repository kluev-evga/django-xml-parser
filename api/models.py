from django.db import models


class Mark(models.Model):
    name = models.CharField(
        'Марка автомобиля',
        max_length=255)


class Model(models.Model):
    name = models.CharField(
        'Модель автомобиля',
        max_length=255)
    mark = models.ForeignKey(
        Mark,
        on_delete=models.CASCADE,
        null=False)

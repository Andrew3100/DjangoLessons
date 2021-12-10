from django.db import models


# Create your models here.
class User(models.Model):
    department = models.TextField('Организация', max_length=1000)
    login = models.TextField('Логин', max_length=1000)
    last_access = models.TextField('Активность', max_length=1000)

    def __str__(self):
        return self.department

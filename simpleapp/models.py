from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

class News(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True, # названия новостей не должны повторяться
    )

    author = models.CharField(
        max_length=50, null=True)

    data = models.CharField(
        max_length=50, null=True)

    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)], null=True)



    def __str__(self):
        return f'{self.name.title()}: {self.description[:10]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


    # поле категории будет ссылаться на модель категории


    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news', # все продукты в категории будут доступны через поле products
    )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


# Категория, к которой будет привязываться товар



class Category(models.Model):
    # названия категорий тоже не должны повторяться


    name = models.CharField(max_length=100, unique=True)

    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name





# Добавили
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user

from django.db import models
from datetime import datetime

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    context = models.TextField()

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

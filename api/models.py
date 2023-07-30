from django.db import models


class User(models.Model):
    id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)


class Service(models.Model):
    title = models.CharField(max_length=100)
    context = models.TextField()

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
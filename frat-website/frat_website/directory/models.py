from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    brother_letters = models.CharField(max_length=23)

    def __str__(self):
        return self.user.username

class ValidEntry(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    brother_letters = models.CharField(max_length=21)

    class Meta:
        unique_together = ('first_name', 'last_name', 'phone_number', 'brother_letters')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

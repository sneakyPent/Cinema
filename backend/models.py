from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
	Title = models.CharField(max_length=100)
	StartDate = models.DateField()
	EndDate = models.DateField()
	Cinema = models.ForeignKey(to='Cinema', on_delete=models.CASCADE, related_name='Cinema', blank=True, null=True)
	Category = models.CharField(max_length=100)


class Cinema(models.Model):
	Owner = models.CharField(max_length=100)
	Name = models.CharField(max_length=100)


class Favorite(models.Model):
	User = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='User', blank=True, null=True)
	Movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE, related_name='Movie', blank=True, null=True)


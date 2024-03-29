from enum import Enum

from django.db import models

from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class Movie(models.Model):
	title = models.CharField(max_length=100)
	startDate = models.DateField()
	endDate = models.DateField()
	cinema = models.ForeignKey(to='Cinema', on_delete=models.CASCADE, related_name='Cinema', blank=True, null=True)
	category = models.CharField(max_length=100)
	availability = models.BooleanField(default=False)


class Cinema(models.Model):
	owner = models.CharField(max_length=100)
	name = models.CharField(max_length=100)


class Favorite(models.Model):
	user = models.CharField(max_length=100)
	movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE, related_name='Movie', blank=True, null=True)


class Request(models.Model):
	userId = models.CharField(max_length=100)
	userName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	role = models.CharField(max_length=100)
	cinema = models.CharField(max_length=100)
	is_active = models.BooleanField(default=False)

class UserSubscriptions(models.Model):
	user = models.CharField(max_length=100)
	notification = models.ForeignKey(to='Notifications', on_delete=models.CASCADE, related_name='SubscriptionMovie', blank=True, null=True)
	seen = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now=True)

class Notifications(models.Model):
	subscription = models.CharField(max_length=100)
	movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE, related_name='NotificationMovie', blank=True, null=True)
	notification = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True)
from enum import Enum

from django.db import models

from django.contrib.auth.models import User, AbstractUser


# Create your models here.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Movie(models.Model):
	title = models.CharField(max_length=100)
	startDate = models.DateField()
	endDate = models.DateField()
	cinema = models.ForeignKey(to='Cinema', on_delete=models.CASCADE, related_name='Cinema', blank=True, null=True)
	category = models.CharField(max_length=100)


class Cinema(models.Model):
	owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='Owner', blank=True, null=True)
	name = models.CharField(max_length=100)


class Favorite(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='User', blank=True, null=True)
	movie = models.ForeignKey(to='Movie', on_delete=models.CASCADE, related_name='Movie', blank=True, null=True)


class UserProfile(models.Model):
	role = models.CharField(max_length=100)
	user = models.OneToOneField(User, on_delete=models.CASCADE,)

	def __unicode__(self):
		return self.user.username

	@receiver(post_save, sender=User)
	def create_profile_for_user(sender, instance=None, created=False, **kargs):
		if created:
			UserProfile.objects.get_or_create(user=instance)

	@receiver(pre_delete, sender=User)
	def delete_profile_for_user(sender, instance=None, **kargs):
		if instance:
			user_profile = UserProfile.objects.get(user=instance)
			user_profile.delete()

from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from backend.models import Favorite
from backend.models import Movie
from backend.models import Cinema


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
	class Meta:
		model = Movie
		fields = '__all__'


class CinemaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cinema
		fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favorite
		fields = '__all__'

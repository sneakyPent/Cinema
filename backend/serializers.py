from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from backend.models import Favorite
from backend.models import Movie
from backend.models import Cinema
from backend.models import UserProfile


class MovieSerializer(serializers.ModelSerializer):
	cinema = serializers.CharField(source='cinema.name', read_only=True)

	class Meta:
		model = Movie
		depth = 1
		fields = (
			'id',
			'title',
			'startDate',
			'endDate',
			'category',
			'cinema',
		)


class CinemaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cinema
		fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
	user = serializers.IntegerField(source='user.id')
	title = serializers.CharField(source='movie.title', read_only=True)
	startDate = serializers.CharField(source='movie.startDate', read_only=True)
	endDate = serializers.CharField(source='movie.endDate', read_only=True)
	category = serializers.CharField(source='movie.category', read_only=True)
	cinema = serializers.CharField(source='movie.cinema.name', read_only=True)

	class Meta:
		model = Favorite
		depth = 1
		fields = (
			'id',
			'user',
			'title',
			'startDate',
			'endDate',
			'category',
			'cinema',
		)


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		depth = 1
		fields = (
			'id',
			'username',
			'first_name',
			'last_name',
			'email',
			'is_superuser',
			'is_staff',
			'is_active',
			'groups'
		)


class UserProfileSerializer(serializers.ModelSerializer):
	# user = serializers.ReadOnlyField(source='user.id')
	id = serializers.IntegerField(source='pk', read_only=True)
	username = serializers.CharField(source='user.username', read_only=True)
	email = serializers.CharField(source='user.email')
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	is_active = serializers.CharField(source='user.is_active')
	cinema = serializers.SerializerMethodField('find_cinema', allow_null=True)

	def find_cinema(self, user):
		up = UserProfile.objects.get(id=user.id)
		if up.role == 'owner':
			cn = list(Cinema.objects.filter(owner_id=user.id)).pop()
			return cn.name
		else:
			return '-'

	class Meta:
		model = UserProfile
		depth = 1
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'role', 'cinema')

	def get_full_name(self, obj):
		request = self.context['request']
		return request.user.get_full_name()

	def update(self, instance, validated_data):
		# retrieve the User
		user_data = validated_data.pop('user', None)
		for attr, value in user_data.items():
			setattr(instance.user, attr, value)

		# retrieve Profile
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.user.save()
		instance.save()
		return instance

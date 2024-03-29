from rest_framework import serializers

from backend.models import Favorite
from backend.models import Movie
from backend.models import Cinema
from backend.models import Request
from backend.models import Notifications
from backend.models import UserSubscriptions


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
			'availability'
		)


class CinemaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cinema
		fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = Request
		depth = 1
		fields = (
			'id',
			'userName',
			'email',
			'role',
			'cinema',
			'is_active'
		)


class FavoriteSerializer(serializers.ModelSerializer):
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


class UserSubscriptionsSerializer(serializers.ModelSerializer):
	title = serializers.CharField(source='notification.movie.title', read_only=True)

	class Meta:
		model = UserSubscriptions
		depth = 1
		fields = (
			'user',
			'title',
		)

class NotificationsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notifications
		fields = '__all__'

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from backend.models import User
from backend.models import Cinema
from backend.models import Movie
from backend.models import Favorite
from backend.models import UserProfile

# from backend.models import
from cinema.settings import bcolors


class Command(BaseCommand):
	def handle(self, **options):
		print('- Init Favorites: ', end='')

		try:
			f = Favorite()
			u = User.objects.get(username='user1')
			m = Movie.objects.get(Title='Bad Boys 1')
			f.Movie = m
			f.User = u
			f.save()

			# -----------------------------------------------------------
			f = Favorite()
			u = User.objects.get(username='user1')
			m = Movie.objects.get(Title='Bad Boys 2')
			f.Movie = m
			f.User = u
			f.save()

			# -----------------------------------------------------------
			f = Favorite()
			u = User.objects.get(username='user2')
			m = Movie.objects.get(Title='Borat 1')
			f.Movie = m
			f.User = u
			f.save()

			# -----------------------------------------------------------

			print(f'{bcolors.BOLD}{bcolors.OKGREEN}OK{bcolors.ENDC}')
		except Exception as e:
			print(f'{bcolors.FAIL}Error! {e}{bcolors.ENDC}')

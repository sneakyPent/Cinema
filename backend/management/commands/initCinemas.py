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
		print('- Init Cinemas: ', end='')

		try:
			c = Cinema()
			u = User.objects.get(username='owner1')
			c.owner = u
			c.name = 'Talos'
			c.save()
			# -----------------------------------------------------------

			c = Cinema()
			u = User.objects.get(username='owner2')
			c.owner = u
			c.name = 'Astoria'
			c.save()
			# -----------------------------------------------------------

			print(f'{bcolors.BOLD}{bcolors.OKGREEN}OK{bcolors.ENDC}')
		except Exception as e:
			print(f'{bcolors.FAIL}Error! {e}{bcolors.ENDC}')

from datetime import datetime
from time import strptime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.db import models
from django.utils import timezone

from backend.models import Cinema
from backend.models import Movie

from cinema.settings import bcolors


class Command(BaseCommand):
	def handle(self, **options):
		print('- Init Movies: ', end='')
		Cinema_1 = 'Talos'
		Cinema_2 = 'Astoria'

		try:

			c = Cinema.objects.get(name=Cinema_1)
			m = Movie()
			m.title = 'Bad Boys 1'
			m.startDate = datetime.strptime('6/11/2020', '%d/%m/%Y')
			m.endDate = datetime.strptime('6/12/2020', '%d/%m/%Y')
			m.cinema = c
			m.category = 'Action'
			m.save()
			# -----------------------------------------------------------
			c = Cinema.objects.get(name=Cinema_1)
			m = Movie()
			m.title = 'Bad Boys 2'
			m.startDate = datetime.strptime('7/11/2020', '%d/%m/%Y')
			m.endDate = datetime.strptime('7/12/2020', '%d/%m/%Y')
			m.cinema = c
			m.category = 'Action'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(name=Cinema_1)
			m = Movie()
			m.title = 'Bad Boys 3'
			m.startDate = datetime.strptime('8/11/2020', '%d/%m/%Y')
			m.endDate = datetime.strptime('8/12/2020', '%d/%m/%Y')
			m.cinema = c
			m.category = 'Action'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(name=Cinema_2)
			m = Movie()
			m.title = 'Borat 1'
			m.startDate = datetime.strptime('9/11/2020', '%d/%m/%Y')
			m.endDate = datetime.strptime('9/12/2020', '%d/%m/%Y')
			m.cinema = c
			m.category = 'Comedy'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(name=Cinema_2)
			m = Movie()
			m.title = 'Borat 2'
			m.startDate = datetime.strptime('10/11/2020', '%d/%m/%Y')
			m.endDate = datetime.strptime('10/12/2020', '%d/%m/%Y')
			m.cinema = c
			m.category = 'Comedy'
			m.save()
			# -----------------------------------------------------------

			print(f'{bcolors.BOLD}{bcolors.OKGREEN}OK{bcolors.ENDC}')
		except Exception as e:
			print(f'{bcolors.FAIL}Error! {e}{bcolors.ENDC}')

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

		try:
			c = Cinema.objects.get(Name='Cinema_1')
			m = Movie()
			m.Title = 'Bad Boys 1'
			m.StartDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.EndDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.Cinema = c
			m.Category = 'Action'
			m.save()
			# -----------------------------------------------------------
			c = Cinema.objects.get(Name='Cinema_1')
			m = Movie()
			m.Title = 'Bad Boys 2'
			m.StartDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.EndDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.Cinema = c
			m.Category = 'Action'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(Name='Cinema_1')
			m = Movie()
			m.Title = 'Bad Boys 3'
			m.StartDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.EndDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.Cinema = c
			m.Category = 'Action'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(Name='Cinema_2')
			m = Movie()
			m.Title = 'Borat 1'
			m.StartDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.EndDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.Cinema = c
			m.Category = 'Comedy'
			m.save()
			# -----------------------------------------------------------

			c = Cinema.objects.get(Name='Cinema_2')
			m = Movie()
			m.Title = 'Borat 2'
			m.StartDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.EndDate = datetime.strptime('20/10/2020', '%d/%m/%Y')
			m.Cinema = c
			m.Category = 'Comedy'
			m.save()
			# -----------------------------------------------------------

			print(f'{bcolors.BOLD}{bcolors.OKGREEN}OK{bcolors.ENDC}')
		except Exception as e:
			print(f'{bcolors.FAIL}Error! {e}{bcolors.ENDC}')

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from backend.models import User
from backend.models import UserProfile



# from backend.models import
from cinema.settings import bcolors


class Command(BaseCommand):
	def handle(self, **options):
		print('- Init Test Users: ', end='')

		try:

			u = User()
			u.first_name = 'Νικόλας'
			u.last_name = 'Ζαχαριουδάκης'
			u.username = 'user1'
			u.email = 'user1@yahoo.com'
			u.set_password('mousakas')
			u.is_active = True
			u.is_staff = False
			u.is_superuser = False
			u.save()
			# groups = [Group.objects.get(name='User')]
			# u.groups.set(groups)
			# u.save()

			p = UserProfile.objects.get(user=u)
			p.role = 'user'
			p.save()

			# -----------------------------------------------------------
			u = User()
			u.first_name = 'Γιώργος'
			u.last_name = 'Ζαχαριουδάκης'
			u.username = 'user2'
			u.email = 'user2@yahoo.com'
			u.set_password('mousakas')
			u.is_active = True
			u.is_staff = False
			u.is_superuser = False
			u.save()
			# groups = [Group.objects.get(name='User')]
			# u.groups.set(groups)
			# u.save()

			p = UserProfile.objects.get(user=u)
			p.role = 'user'
			p.save()

			# -----------------------------------------------------------

			u = User()
			u.first_name = 'Βασίλης'
			u.last_name = 'Ζαχαριουδάκης'
			u.username = 'owner1'
			u.email = 'owner1@yahoo.com'
			u.set_password('mousakas')
			u.is_active = True
			u.is_staff = False
			u.is_superuser = False
			u.save()
			# groups = [Group.objects.get(name='CinemaOwner')]
			# u.groups.set(groups)
			# u.save()

			p = UserProfile.objects.get(user=u)
			p.role = 'owner'
			p.save()

			# -----------------------------------------------------------
			u = User()
			u.first_name = 'Γιάννης'
			u.last_name = 'Ζαχαριουδάκης'
			u.username = 'owner2'
			u.email = 'owner2@yahoo.com'
			u.set_password('mousakas')
			u.is_active = True
			u.is_staff = False
			u.is_superuser = False
			u.save()
			# groups = [Group.objects.get(name='CinemaOwner')]
			# u.groups.set(groups)
			# u.save()

			p = UserProfile.objects.get(user=u)
			p.role = 'owner'
			p.save()

			# -----------------------------------------------------------
			u = User()
			u.first_name = 'Aντώνης'
			u.last_name = 'Ζαχαριουδάκης'
			u.username = 'admin'
			u.email = 'admin@yahoo.com'
			u.set_password('mousakas')
			u.is_active = True
			u.is_staff = True
			u.is_superuser = False
			u.save()
			# groups = [Group.objects.get(name='Admin')]
			# u.groups.set(groups)
			# u.save()

			p = UserProfile.objects.get(user=u)
			p.role = 'admin'
			p.save()

			# -----------------------------------------------------------
			u = User()
			u.first_name = ''
			u.last_name = ''
			u.username = 'master'
			u.email = 'master@yahoo.com'
			u.set_password('mousakas')
			u.is_active=True
			u.is_staff=True
			u.is_superuser=True
			u.save()
			# groups = [Group.objects.get(name='ViewEnumerators'), Group.objects.get(name='EditEnumerators'),
			# 			Group.objects.get(name='CinemaOwner'), Group.objects.get(name='User'),
			# 			Group.objects.get(name='Admin'), ]
			# u.groups.set(groups)
			u.save()
			print(f'{bcolors.BOLD}{bcolors.OKGREEN}OK{bcolors.ENDC}')
		except Exception as e:
			print(f'{bcolors.FAIL}Error! {e}{bcolors.ENDC}')

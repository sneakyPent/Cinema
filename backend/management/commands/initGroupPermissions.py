import json
import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from cinema.settings import BASE_DIR
from django.db import connection


def resetSequence(name):
	sql = "update sqlite_sequence set seq=0 where name like '%" + name + "'"
	with connection.cursor() as cursor:
		cursor.execute(sql)


class Command(BaseCommand):
	def handle(self, **options):
		print('- Init User Groups: ', end='')

		try:
			Group.objects.all().delete()
			resetSequence('group')
			resetSequence('group_permissions')

			f = open(os.path.join(BASE_DIR, 'backend/management/initData/groupPermissions.json'), 'r', encoding="utf8")
			f = json.loads(f.read())
			for group in f:
				new_group, created = Group.objects.get_or_create(name=group)
				for per in f[group]:
					permission = Permission.objects.get(codename=per)
					new_group.permissions.add(permission)
			print(f' \033[1m \033[92m OK \033[0m')
		except Exception as e:
			print(f' \033[91m Error! {e} \033[0m')

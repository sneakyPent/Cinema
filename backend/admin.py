from django.contrib import admin

# Register your models here.
from backend.models import Favorite
from backend.models import Cinema
from backend.models import Movie

admin.site.register(Favorite)
admin.site.register(Cinema)
admin.site.register(Movie)

from django.contrib import admin
from .models import Film, Projection, RapportHebdomadaire, User

admin.site.register(Film)
admin.site.register(Projection)
admin.site.register(RapportHebdomadaire)
admin.site.register(User)
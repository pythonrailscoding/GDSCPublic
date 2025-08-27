from django.contrib import admin

from .models import VerifyMembers, Profile

admin.site.register(VerifyMembers)
admin.site.register(Profile)

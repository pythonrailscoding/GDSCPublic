from django.contrib import admin

from . import models

admin.site.register(models.BlogModel)
admin.site.register(models.Comment)

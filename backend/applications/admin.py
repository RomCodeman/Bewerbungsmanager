from django.contrib import admin

from .models import Application, Company

# Register your models here.
admin.site.register(Company)
admin.site.register(Application)

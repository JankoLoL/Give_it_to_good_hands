from django.contrib import admin
from good_hands_app.models import Category, Institution, Donation, InstitutionCategory


myModels = [Institution, Donation, Category, InstitutionCategory]  # iterable list

admin.site.register(myModels)


# Register your models here.

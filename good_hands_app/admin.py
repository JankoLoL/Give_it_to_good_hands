from django.contrib import admin
from good_hands_app.models import Category, Institution, Donation


myModels = [Institution, Donation, Category]  # iterable list

admin.site.register(myModels)


# Register your models here.

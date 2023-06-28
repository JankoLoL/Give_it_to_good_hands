from django.db import models
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    INSTITUTION_TYPE = [
        ("fundacja", "fundacja"),
        ("organizacja pozarządowa", "organizacja pozarządowa"),
        ("zbiórka lokalna", "zbiórka lokalna"),
    ]
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = forms.ChoiceField(choices=INSTITUTION_TYPE, initial="fundacja")
    categories = models.ManyToManyField(Category)

from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from good_hands_app.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(bags_sum_quantity=Sum('quantity'))['bags_sum_quantity']
        if bags_quantity is None:
            bags_quantity = 0
        institutions_quantity = Institution.objects.all().count()
        if institutions_quantity is None:
            institutions_quantity = 0
        context = {
            'bags_quantity': bags_quantity,
            'institutions_quantity': institutions_quantity,
        }
        return render(request, "index.html", context)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")
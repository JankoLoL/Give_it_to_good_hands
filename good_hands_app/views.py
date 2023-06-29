from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from good_hands_app.models import Donation


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(bags_sum_quantity=Sum('quantity'))['bags_sum_quantity']
        context = {
            'bags_quantity': bags_quantity,
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
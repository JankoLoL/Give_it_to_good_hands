from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request):
        return render(request, "index.html")


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")

    def post(self, request):
        return render(request, "form-confirmation.html")
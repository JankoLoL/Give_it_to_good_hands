from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from good_hands_app.models import Donation, Institution,Category


class LandingPageView(View):
    def get(self, request):
        bags_quantity = Donation.objects.aggregate(bags_sum_quantity=Sum('quantity'))['bags_sum_quantity']
        if bags_quantity is None:
            bags_quantity = 0
        institutions_quantity = Institution.objects.all().count()
        if institutions_quantity is None:
            institutions_quantity = 0

        institutions = Institution.objects.all()
        institution_type = institutions.values('type').distinct()
        context = {
            'bags_quantity': bags_quantity,
            'institutions_quantity': institutions_quantity,
            'institutions': institutions,
            'institution_type': institution_type,
        }
        return render(request, "index.html", context)


class AddDonationView(LoginRequiredMixin, View):
    login_url = '/login/'


    def get(self, request):
        categories = Category.objects.all()
        return render(request, "form.html", {'categories': categories})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if (email, password) is not None:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('landing-page')
            else:
                return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "index.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            redirect('register')
        if (name, surname, email, password, password2) is not None:
            user = User.objects.create_user(first_name=name, last_name=surname, email=email, password=password,
                                            username=email)
            user.save()
            return redirect('login')

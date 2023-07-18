from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Sum
from good_hands_app.models import Donation, Institution, Category, InstitutionCategory


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
        institutions = Institution.objects.all()
        # institution_category = InstitutionCategory.objects.all()

        context = {
            'categories': categories,
            'institutions': institutions,
            # 'institution_category': institution_category,
        }
        return render(request, "form.html", context)

    def post(self, request):
        quantity = request.POST.get('bags')
        categories = request.POST.getlist('categories')
        institution = request.POST.get('organization')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        if (quantity, categories, institution, address, phone_number, city, zip_code, pick_up_date, pick_up_time,
            pick_up_comment, user) is not None:
            donation = Donation.objects.create(quantity=quantity, institution_id=institution, address=address,
                                               phone_number=phone_number, city=city, zip_code=zip_code,
                                               pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment, user=user)
            donation.categories.set(categories)
            donation.save()
            return render(request, "form-confirmation.html")
        else:
            return redirect('add-donation')


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
                return redirect('profile')
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


class UserView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        context = {
            'donations': Donation.objects.filter(user=request.user)
        }
        return render(request, "user.html", context=context)


class UserEditView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            context = {
                'user': user,
            }
            return render(request, "user-edit.html", context=context)
        except User.DoesNotExist:
            return redirect('/404/')

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.first_name = request.POST.get('name')
        user.last_name = request.POST.get('surname')
        user.email = request.POST.get('email')

        if not (user.first_name and user.last_name and user.email):
            messages.error(request, "Wszystkie pola muszą być wypełnione.")
            return redirect('profile-edit', pk=pk)

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        if old_password and user.check_password(old_password):
            if new_password == new_password2:
                user.set_password(new_password)
            else:
                messages.error(request, "Nowe hasła nie są identyczne. Proszę wprowadzić identyczne hasła.")
                return redirect('profile-edit', pk=pk)

        user.save()
        messages.success(request, "Dane użytkownika zostały pomyślnie zaktualizowane.")
        return redirect('profile')
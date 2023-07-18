"""
URL configuration for GoodHandsProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from good_hands_app.views import LandingPageView, AddDonationView, LoginView, LogoutView, RegisterView, UserView, \
    UserEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('form/', AddDonationView.as_view(), name='donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserView.as_view(), name='profile'),
    path('profile/<int:pk>/', UserEditView.as_view(), name='profile-edit'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView,
    AboutPageView,
    SignInPageView,
    ForgotPassPageView,
    ContactPageView,
    ProductListView,
    ProductDetailView,
    UserRegistrationView,
    ProfileView,
    ChangePasswordView,
    DeleteAccountView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('signin/', SignInPageView.as_view(), name='signin'),
    path('forgotpass/', ForgotPassPageView.as_view(), name='forgotpass'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('menu/', ProductListView.as_view(), name='menu'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('changepass/', ChangePasswordView.as_view(), name='changepass'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]

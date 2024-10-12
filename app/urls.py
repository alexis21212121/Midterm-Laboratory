from django.urls import path
from .views import HomePageView, AboutPageView, SignInPageView, SignUpPageView, ForgotPassPageView, ContactPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('signin/', SignInPageView.as_view(), name='signin'),
    path('signup/', SignUpPageView.as_view(), name='signup'),
    path('forgotpass/', ForgotPassPageView.as_view(), name='forgotpass'),
    path('contact/', ContactPageView.as_view(), name='contact'),
]
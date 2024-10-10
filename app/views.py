from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class SignInPageView(TemplateView):
    template_name = 'app/signin.html'

class SignUpPageView(TemplateView):
    template_name = 'app/signup.html'

class ForgotPassPageView(TemplateView):
    template_name = 'app/forgotpass.html'
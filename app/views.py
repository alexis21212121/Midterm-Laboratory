from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from .models import UserProfile
from django.contrib.auth.models import User
from .models import UserProfile, Product
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django import forms
from django.contrib.auth import update_session_auth_hash


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class ProfileView(TemplateView):
    template_name = 'app/profile_view.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ForgotPassPageView(TemplateView):
    template_name = 'app/forgotpass.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'


class ContactPageView(TemplateView):
    template_name = 'app/contact.html'


class ProductListView(ListView):
    model = Product
    template_name = 'app/menu.html'
    context_object_name = 'products'

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'app/signup.html'
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        """Override form_valid to log the user in after successful registration."""
        user = form.save() 

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Redirect to home if the user is already logged in."""
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'


class SignInPageView(View):
    def get(self, request):
        """Render the sign-in page on GET request."""
        return render(request, 'app/signin.html')

    def post(self, request):
        """Handle the login logic on POST request."""
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)  
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')  
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'app/signin.html')


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data



class ChangePasswordView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangePasswordForm  
    template_name = 'app/change_password.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()

       
        update_session_auth_hash(self.request, user)

        messages.success(self.request, "Your password has been successfully changed.")
        
  
        return redirect('home')

    def get_success_url(self):
        return reverse_lazy('home')



class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'app/delete_account.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user
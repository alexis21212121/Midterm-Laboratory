from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Product

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Enter email"}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={"placeholder": "Enter phone number"}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={"placeholder": "Enter your address"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()

        
            user_profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': self.cleaned_data.get('phone_number'),
                    'address': self.cleaned_data.get('address'),
                }
            )
            
            if not created:
     
                user_profile.phone_number = self.cleaned_data.get('phone_number')
                user_profile.address = self.cleaned_data.get('address')
                user_profile.save()
        
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'stock', 'categories']
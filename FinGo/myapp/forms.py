from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  # Add this import
from .models import UserProfile, Product

class RegisterForm(UserCreationForm):  # Change from ModelForm to UserCreationForm
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    birthdate = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    contact_no = forms.CharField(max_length=20, required=False)
    address = forms.CharField(
        max_length=190, 
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
            # Create or update UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.birthdate = self.cleaned_data.get('birthdate')
            profile.contact_no = self.cleaned_data.get('contact_no')
            profile.address = self.cleaned_data.get('address')
            profile.save()
            
        return user
    
# forms.py
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "birthdate", "contact_no", "address"]

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", "productName", "description","price", "stock",  ]

       
    

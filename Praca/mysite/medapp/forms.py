from django import forms
from django.contrib.auth.models import User
from django.forms import fields, ModelForm
from django.forms.fields import EmailField
from .models import Contact, Product, Category, Profile, Order


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def clean_password2(self): #sprawdzenie czy podane hasła są identyczne
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne')
        return cd['password2']    
    
    def clean_email(self): #sprawdzenie w bazie danych czy email już jest używany
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email już istnieje")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'image')

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class OrderFrom(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('quantity', 'days', 'name1','name2','phone_number','home_number','apartment','postcode', 'city_name')
from django import forms
from django.contrib.auth.models import User
from .models import Contact, Profile, Order


class UserRegisterForm(forms.ModelForm):
    """
    A form for user registration. Includes email, username, and password fields.
    It verifies that the provided passwords match and ensures the email is unique.
    """
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('email', 'username',)

    def clean_password2(self): 
        """
        Validate that both password fields match.
        Raises a validation error if they do not.
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne')
        return cd['password2']    
    
    def clean_email(self): 
        """
        Check if the provided email is already in use.
        Raises a validation error if the email is found in the database.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email już istnieje")
        return email


class UserEditForm(forms.ModelForm):
    """
    Form for editing a User instance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Adres e-mail'
        }


class ProfileEditForm(forms.ModelForm):
    """
    Form for editing a Profile instance.
    """
    class Meta:
        model = Profile
        fields = ('description', 'image')
        labels ={
            'description': 'Opis profilu',
            'image': 'Zdjęcie profilowe'
        }

class ContactForm(forms.ModelForm):
    """
    Form for submitting contact information.
    """
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {
            'email_guest': 'Adres e-mail',
            'topic': 'Temat',
            'message_text': ' Twoja wiadomość'
        }

class OrderFrom(forms.ModelForm):
    """
    Form for creating or editing an Order instance.
    """
    class Meta:
        model = Order
        fields = ('quantity', 'days', 'name1','name2','phone_number','home_number','apartment','postcode', 'city_name')
        labels ={
            'quantity':'Ilość', 
            'days': 'Ilość dni', 
            'name1': 'Imię',
            'name2': 'Nazwisko',
            'phone_number': 'Numer telefonu',
            'home_number': 'Adres',
            'apartment': 'Numer mieszkania',
            'postcode': 'Kod pocztowy', 
            'city_name': 'Miasto'
        }
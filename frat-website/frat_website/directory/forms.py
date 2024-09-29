from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ValidEntry

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    brother_letters = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'brother_letters', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        phone_number = cleaned_data.get('phone_number')
        brother_letters = cleaned_data.get('brother_letters')

        if not ValidEntry.objects.filter(first_name=first_name, last_name=last_name, phone_number=phone_number, brother_letters=brother_letters).exists():
            raise forms.ValidationError("Your details do not match our records. Please contact the administrator.")

        # Ensure these details haven't been used already
        if User.objects.filter(first_name=first_name, last_name=last_name, profile__phone_number=phone_number, profile__brother_letters=brother_letters).exists():
            raise forms.ValidationError("These details have already been used to sign up.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                brother_letters=self.cleaned_data['brother_letters']
            )
        return user

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

class ValidEntryForm(forms.ModelForm):
    class Meta:
        model = ValidEntry
        fields = ['first_name', 'last_name', 'phone_number', 'brother_letters']

class ValidEntryImportForm(forms.Form):
    file = forms.FileField()

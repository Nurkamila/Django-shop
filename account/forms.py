import email
from django.forms import ModelForm, CharField, PasswordInput, ValidationError
from django.contrib.auth import get_user_model
from .helpers import send_activation_mail

User = get_user_model()

class RegistrationForm(ModelForm):
    password = CharField(min_length=6, max_length=20, required=True, widget=PasswordInput)
    password_confirmation = CharField(min_length=6, max_length=20, required=True, widget=PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirmation')

    def clean_email(self):
        username = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with given name already exists')
        return username

    def clean(self):
        data = self.cleaned_data
        password1 = data.get('password')
        password2 = data.get('password_confirmation')
        if password1 != password2:
            raise ValidationError('Password does not match')
        return data

    def save(self):
        user = super().save()
        send_activation_mail(user)
        return user
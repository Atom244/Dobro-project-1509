from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']
        labels = {'first_name': 'Имя', 'email': 'Email'}

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirm'):
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

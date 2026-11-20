import re

from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

PHONE_PATTERN = r"(8|\+7)\d{10}"
PHONE_RE = re.compile(PHONE_PATTERN)
PHONE_PREFIX = "+7"
PHONE_DIGITS = 10


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("name", "surname", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Неверный имейл или пароль")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        widgets = {
            "avatar": forms.FileInput,
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return None
        if not PHONE_RE.fullmatch(phone):
            raise forms.ValidationError(
                "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
            )
        phone = PHONE_PREFIX + phone[-PHONE_DIGITS:]
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот номер телефона уже используется")
        return phone

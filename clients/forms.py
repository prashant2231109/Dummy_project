from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


from .models import Company, Subscriber
from source.models import Source
from story.models import Story


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        error_messages={"required": "Username is required"},
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    confirm_password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "url", "source", "body_text", "tagged_companies"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        company = self.request.user.subscriber.company
        if Story.objects.filter(url=url, company=company).exists():
            raise ValidationError(
                "Story with this URL already exists for your company."
            )
        return cleaned_data


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["name", "url", "tagged_companies"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        company = self.request.user.subscriber.company
        if Source.objects.filter(url=url, company=company).exists():
            raise ValidationError(
                "Source with this URL already exists for your company."
            )
        return cleaned_data

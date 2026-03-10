from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User

from source.models import Source

from .forms import LoginForm, SignupForm
from .models import Company, Subscriber


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            if User.objects.filter(username=data["username"]).exists():
                messages.error(request, "Username already exists")
                return render(request, "clients/signup.html", {"form": form})

            if data["password"] != data["confirm_password"]:
                messages.error(request, "Passwords do not match")
                return render(request, "clients/signup.html", {"form": form})

            user = User.objects.create_user(
                username=data["username"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
            )
            messages.success(request, "Signup successful")

            company = data["company"]

            Subscriber.objects.create(user=user, company=company)
            return redirect("login")

    else:
        form = SignupForm()
    return render(request, "clients/signup.html", {"form": form})


def login_view(request):
    print(request)
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(request.POST)
        print(request.user)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # print("CSRF Token:", request.META.get("SESSION_COOKIE"))
                # print("User authenticated successfully")
                # print("CSRF Token:", request.META.get("CSRF_COOKIE"))
                messages.success(request, "Login successful")
                if Source.objects.filter(
                    company=request.user.subscriber.company
                ).exists():
                    return redirect("story:list")

                return redirect("add_source")

            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "clients/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")

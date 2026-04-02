from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from source.models import Source
from subscriber.forms import LoginForm, SignupForm
from subscriber.models import Subscriber





def signup_view(request):
    """view handle user regisration and create subscriber profile
    linked to a company."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data["username"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                )

                company = data["company"]

                Subscriber.objects.create(user=user, company=company)
                return redirect("login")

    else:
        form = SignupForm()
    return render(request, "users/signup.html", {"form": form})

    


def login_view(request):
    """view handle user login and redirect to story list if user has sources"""

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                user = User.objects.select_related("subscriber").get(id=user.id)

                login(request, user)

                if (
                    Source.objects.select_related("company")
                    .filter(company=request.user.subscriber.company)
                    .exists()
                ):

                    # return redirect("story:list")

                    return redirect("/stories/new/")

                # return redirect("source:add")
                
                return redirect("/sources/new/")
                

            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")







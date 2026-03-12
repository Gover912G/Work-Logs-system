# from django.shortcuts import render

# # Create your views here.
# def login_view(request):
#     return render(request, 'accounts/login.html', {"title": "Login"})

# def logout_view(request):
#     pass

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib.auth.models import User


def signup_view(request):

    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect("accounts:login")

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("logs:dashboard")

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)
    return redirect("accounts:login")
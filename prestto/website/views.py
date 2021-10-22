from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .form import *


# Create your views here.

def homepage(request):
    """
    renders the homepage
    :param request:
    :return:
    """
    return render(request, template_name="website/index.html")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST, auto_id=True)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password_1")

            # todo : send email

            user = authenticate(username=username, password=password)
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))

            return redirect(homepage)

    return render(request, 'website/')


def partner_sign_up(request):
    pass


def sign_in(request):
    pass

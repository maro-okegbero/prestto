from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .form import *

# Create your views here.
from .models import BusinessName, LimitedLiability


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


@login_required(login_url="/login")
def admin_page(request):
    """

    :param request:
    :return:
    """
    user = request.user
    business_name_applications = BusinessName.objects.all()
    context = {"business_names": business_name_applications, "user": user}
    return render(request, 'website/presto_dashboard.html', context)


@login_required(login_url="/login")
def ltd_requests(request):
    """

    :param request:
    :return:
    """
    user = request.user
    lt_requests = LimitedLiability.objects.all()
    context = {"ltd_requests": lt_requests, "user": user}
    return render(request, 'website/LTD.html', context)


@login_required(login_url="/login")
def business_name_detail(request, pk):
    """

    :param pk:
    :param request:
    :return:
    """
    user = request.user
    application = BusinessName.objects.get(pk=pk)
    context = {"application": application, "user": user}
    return render(request, 'website/business_name_detail.html', context)


def partner_sign_up(request):
    pass


def sign_in(request):
    """
    :param request:
    :return:
    """
    form = LoginUserForm()
    if request.method == "POST":
        form = LoginUserForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # checking to see if there's a next url in the link
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))

                return redirect(admin_page)
            else:
                context = {'error': "The username or password is wrong",
                           'form': form, }
            return render(request, "website/login.html", context)
        else:
            context = {'error': "The username or password is wrong",
                       'form': form, }
            return render(request, "website/login.html", context)

    context = {'error': "",
               'form': form, }
    return render(request, "website/login.html", context)


def sign_out(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return redirect(homepage)

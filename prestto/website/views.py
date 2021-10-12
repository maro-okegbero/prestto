from django.shortcuts import render


# Create your views here.

def homepage(request):
    """
    renders the homepage
    :param request:
    :return:
    """
    return render(request, template_name="website/index.html")


def sign_up(request):
    pass


def sign_in(request):
    pass


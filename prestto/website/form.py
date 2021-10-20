from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name",
                                 widget=forms.TextInput(attrs={'id': 'first_name'}))

    last_name = forms.CharField(max_length=30, required=True, label="Last Name",
                                widget=forms.TextInput(attrs={'id': 'first_name'}))

    email = forms.EmailField(max_length=254, required=True, label="Email",
                             widget=forms.EmailInput(attrs={'id': 'email'}))

    username = forms.CharField(max_length=30, required=True, label="Username",
                               widget=forms.TextInput(attrs={'id': 'username',
                                                             'name': 'username', }))

    business_name = forms.CharField(max_length=30, required=True, label="Business Name",
                                    widget=forms.TextInput(attrs={'id': 'business_name',
                                                                  'name': 'business_name', }))

    business_email = forms.EmailField(max_length=254, required=True, label="Business Email",
                                      widget=forms.EmailInput(attrs={'id': 'business_email'}))

    phone_number = forms.CharField(max_length=11, required=True, label="Phone Number",
                                   widget=forms.TextInput(attrs={'id': 'phone_number'}))

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'phone_number', 'first_name', 'last_name', 'email',
                  'password1', 'password2']


class RegisterPartnerForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, label="Username",
                               widget=forms.TextInput(attrs={'id': 'username',
                                                             'name': 'username', }))

    business_name = forms.CharField(max_length=30, required=True, label="Business Name",
                                    widget=forms.TextInput(attrs={'id': 'business_name',
                                                                  'name': 'business_name', }))

    business_email = forms.EmailField(max_length=254, required=True, label="Business Email",
                                      widget=forms.EmailInput(attrs={'id': 'business_email'}))

    phone_number = forms.CharField(max_length=11, required=True, label="Phone Number",
                                   widget=forms.TextInput(attrs={'id': 'phone_number'}))

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'phone_number', 'business_email', 'business_name',
                  'password1', 'password2']


class BusinessNameRegistration(forms.Form):
    """

    """
    proposed_business_name = forms.CharField(max_length=500, required=False)  # the name the business will be called and  registered with legally
    proposed_company_name = forms.CharField(max_length=500, required=False)  # the alternative if your proposed business name is unavailable
    business_phone_number = forms.CharField(max_length=12, required=False)  # the phone number
    business_email = forms.EmailField(max_length=12, required=False)
    business_address = forms.CharField(max_length=1000, required=False)
    state = forms.CharField(max_length=100, required=False)
    nature_of_business = forms.CharField(max_length=1000, required=False)
    business_commencement_date = forms.DateField(required=False)  # cannot be more than 40 days from the date_created
    is_individual_owner = forms.BooleanField()
    is_corporate_owner = forms.BooleanField()

from rest_framework import serializers

from pprint import pprint
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy, ugettext_lazy
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.db.models import ObjectDoesNotExist, __all__
from ..utils import token_generator, generate_referral_code, send_email_verification_pin


def validate_phone_number(value):
    """
    check that a correct phone_number was inputted
    """
    try:
        _exists = user_model().objects.get(phone_number=value)
    except ObjectDoesNotExist:
        _exists = None

    if len(value) != 11:
        raise serializers.ValidationError('The length of the phone_number is incorrect')
    elif _exists:
        raise serializers.ValidationError('The phone_number provided is already in use!')


def validate_gender(value):
    """
    checks that the correct value for gender is passed
    """
    if value not in ["male", "female"]:
        raise serializers.ValidationError('Incorrect value passed for gender field')


def validate_email(value):
    """
    check to see that a user exist with that email address
    """
    try:
        user = user_model().objects.get(email=value)
    except Exception as e:
        print(e)
        user = None
    if user:
        raise serializers.ValidationError('This email is different from the initial email')


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=True)
    phone_number = serializers.CharField(validators=[validate_phone_number], required=True)
    gender = serializers.CharField(validators=[validate_gender], required=False)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=user_model().objects.all(),
                                                               message="This username is in use, please try a different one")])
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=user_model().objects.all())], max_length=32)
    referee = serializers.CharField(required=False)  # referral code of the affiliate marketer
    password = serializers.CharField(min_length=8, write_only=True)

    # The client should not be able to send a token or points along with a registration
    # request. Making them read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    email_token = serializers.CharField(max_length=255, read_only=True)
    points = serializers.IntegerField(read_only=True)
    referral_code = serializers.CharField(read_only=True)

    #
    # def create(self, validated_data):
    #     """
    #     serializer.save() calls this function
    #     """
    #     token = token_generator()
    #     referral_code = generate_referral_code()
    #     validated_data['email_token'] = token
    #     validated_data['referral_code'] = referral_code
    #     ref_code = validated_data.get("referee", None)
    #
    #     user = user_model().objects.create_user(**validated_data)
    #     name = user.fullname
    #     email = validated_data.get("email")
    #     print("I'm about to send a mail initiation...............................................")
    #     send_email_verification_pin(email=email, pin=token, name=name)
    #
    #     return user

    # def validate_email_address(self, email, token):
    class Meta:
        model = user_model()
        fields = ('id', 'username', 'email', 'password', 'phone_number',
                  'fullname', 'institution', 'date_of_birth', 'gender', 'token', 'points', 'image', 'email_token',
                  'referee', 'referral_code')

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
        raise serializers.ValidationError('The length of the phone_number is incorrect, should be in 080 format')
    elif _exists:
        raise serializers.ValidationError('The phone_number provided is already in use!')


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
    business_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(validators=[validate_phone_number], required=True)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=user_model().objects.all(),
                                                               message="This email is in use, please try a different one")])

    password = serializers.CharField(min_length=8, write_only=True)

    # The client should not be able to send a token or points along with a registration
    # request. Making them read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    email_token = serializers.CharField(max_length=255, read_only=True)

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
        fields = ('id', 'business_name', 'email', 'password', 'phone_number', 'token', 'image', 'email_token')


class LoginSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)
    phone_number = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    image = serializers.URLField(read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid" information. In the case of logging a
        # user in, this means validating that they've provided a username
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        try:
            user = user_model().objects.get(email=email)
            username = user.username
            user = authenticate(username=username, password=password)
        except Exception as e:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        data = dict(
            email=user.email,
            username=user.username,
            token=user.token,
            points=user.points,
            fullname=user.fullname,
            gender=user.gender,
            phone_number=user.phone_number,
            image=user.image
        )
        return data

    def create(self, validated_data):
        return super(LoginSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(LoginSerializer, self).update(validated_data)

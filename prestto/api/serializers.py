from abc import ABC
from datetime import datetime
from pprint import pprint

from django.contrib.auth import get_user_model as user_model
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
import pytz

utc = pytz.UTC


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
            business_name=user.business_name,
            phone_number=user.phone_number,
            image=user.image
        )
        return data

    def create(self, validated_data):
        return super(LoginSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(LoginSerializer, self).update(instance=instance, validated_data=validated_data)


class BusinessNameSerializer(serializers.Serializer):
    """

    """
    proposed_business_name = serializers.CharField(max_length=500,
                                                   required=True)  # the name the business will be called and  registered with legally
    proposed_company_name = serializers.CharField(max_length=500,
                                                  required=True)  # the alternative if your proposed business name is unavailable
    business_phone_number = serializers.CharField(max_length=255, required=True)  # the phone number
    business_email = serializers.EmailField(max_length=100, required=True)
    business_address = serializers.CharField(max_length=1000, required=True)
    state = serializers.CharField(max_length=100, required=True)
    nature_of_business = serializers.CharField(max_length=1000, required=True)
    business_commencement_date = serializers.DateTimeField(
        required=True)  # cannot be more than 40 days from the date_created
    is_individual_owner = serializers.BooleanField(required=True)
    is_corporate_owner = serializers.BooleanField(required=True)
    is_attestee = serializers.BooleanField(required=False)

    individual_surname = serializers.CharField(max_length=200, required=False)
    individual_first_name = serializers.CharField(max_length=200, required=False)
    individual_other_name = serializers.CharField(max_length=200, required=False)
    individual_date_of_birth = serializers.DateField(required=False)
    individual_gender = serializers.CharField(max_length=100, required=False)
    individual_nationality = serializers.CharField(max_length=100, required=False)
    individual_occupation = serializers.CharField(max_length=100, required=False)
    individual_phone_number = serializers.CharField(max_length=255, required=False)  # the phone number
    individual_email = serializers.EmailField(max_length=255, required=False)
    individual_residential_address = serializers.CharField(max_length=1000, required=False)
    individual_means_of_identification = serializers.CharField(max_length=100, required=False)
    # individual_identification = serializers.Field('pdf', )
    # individual_signature = CloudinaryField('image', )
    # individual_photograph = CloudinaryField('image', )
    # individual_other_documents = serializers.ManyToManyField(ExtraDocument)

    attestee_surname = serializers.CharField(max_length=250, required=False)
    attestee_first_name = serializers.CharField(max_length=250, required=False)
    attestee_other_name = serializers.CharField(max_length=250, required=False)
    attestee_date_of_birth = serializers.DateField(required=False)  # cannot be less than 18
    attestee_gender = serializers.CharField(max_length=250, required=False)
    attestee_nationality = serializers.CharField(max_length=100, required=False)
    attestee_phone_number = serializers.CharField(max_length=100, required=False)  # the phone number
    attestee_email = serializers.EmailField(max_length=255, required=False)
    attestee_residential_address = serializers.CharField(max_length=1000, required=False)
    attestee_means_of_identification = serializers.CharField(max_length=100, required=False)
    attestee_identification_number = serializers.CharField(max_length=100, required=False)

    corporate_registration_number = serializers.CharField(max_length=200, required=False)
    corporate_name_of_authorized_signatory = serializers.CharField(max_length=200, required=False)
    corporate_residential_address = serializers.CharField(max_length=1000, required=False)
    corporate_gender = serializers.CharField(max_length=100, required=False)
    corporate_email = serializers.EmailField(max_length=12, required=False)
    corporate_phone_number = serializers.CharField(max_length=12, required=False)  # the phone number
    corporate_means_of_identification = serializers.CharField(max_length=100, required=False)
    # corporate_identification = serializers.CharField(max_length=100, required=False)
    # corporate_signature = serializers.CharField(max_length=100, required=False)
    # corporate_photograph = serializers.CharField(max_length=100, required=False)

    # other_documents = serializers.ManyToManyField(ExtraDocument)

    date_created = serializers.DateTimeField(default=datetime.now())
    last_created = serializers.DateTimeField(default=datetime.now())

    def validate(self, data):
        """
        validate the data sent from the front, this is where the logic for the different fields will be implemented
        :param data:
        :return:

        """
        business_commencement_date = data.get("business_commencement_date")
        is_attestee = data.get("is_attestee", None)
        date_created = data.get("date_created")
        limit_date = date_created + timedelta(days=40)
        print(type(business_commencement_date))
        print(business_commencement_date.year)
        bcd = business_commencement_date.replace(tzinfo=utc)
        ld = limit_date.replace(tzinfo=utc)

        if bcd > ld:
            serializers.DjangoValidationError(
                message={'business_commencement_date': 'this date can be more than 40 days from today'})

        # is_corporate_owner validation
        is_corporate_owner = data.get("is_corporate_owner", None)
        if is_corporate_owner and (not data.get("corporate_registration_number", None)
                                   or not data.get("corporate_name_of_authorized_signatory", None) or
                                   not data.get("corporate_residential_address", None) or not data.get(
                    "corporate_gender", None)
                                   or not data.get("corporate_email", None)
                                   or not data.get("corporate_phone_number", None)
                                   or not data.get("corporate_means_of_identification",
                                                   None)  # or not data.get("corporate_identification")
                # or not data.get("corporate_signature")
                # or not data.get("photograph", None)
        ):
            error_message = {
                "corporate_registration_number": "This field cannot be empty if is_corporate_owner is True",
                "corporate_name_of_authorized_signatory": "This field cannot be empty if is_corporate_owner is True",
                "corporate_residential_address": "This field cannot be empty if is_corporate_owner is True",
                "corporate_email": "This field cannot be empty if is_corporate_owner is True",
                "corporate_gender": "This field cannot be empty if is_corporate_owner is True",
                "corporate_phone_number": "This field cannot be empty if is_corporate_owner is True",
                "corporate_means_of_identification": "This field cannot be empty if is_corporate_owner is True"}
            if data.get("corporate_registration_number", None):
                error_message.pop("corporate_registration_number")

            if data.get("corporate_name_of_authorized_signatory", None):
                error_message.pop("corporate_name_of_authorized_signatory")

            if data.get("corporate_residential_address", None):
                error_message.pop("corporate_residential_address")

            if data.get("corporate_gender", None):
                error_message.pop("corporate_gender")

            if data.get("corporate_email", None):
                error_message.pop("corporate_email")

            if data.get("corporate_phone_number", None):
                error_message.pop("corporate_phone_number")

            if data.get("corporate_means_of_identification", None):
                error_message.pop("corporate_means_of_identification")

            raise serializers.DjangoValidationError(
                message=error_message)

        is_individual_owner = data.get("is_individual_owner")
        if is_individual_owner and (not data.get("individual_surname", None)
                                    or not data.get("individual_first_name", None)
                                    or not data.get("individual_other_name", None)
                                    or not data.get("individual_date_of_birth", None)
                                    or not data.get("individual_gender", None)
                                    or not data.get("individual_nationality", None)
                                    or not data.get("individual_occupation", None)
                                    or not data.get("individual_phone_number", None)
                                    or not data.get("individual_email", None)
                                    or not data.get("individual_residential_address", None)
                                    or not data.get("individual_means_of_identification", None)):
            error_message = {"individual_surname": "This field cannot be empty if is_individual_owner is True",
                             "individual_first_name": "This field cannot be empty if is_individual_owner is True",
                             "individual_other_name": "This field cannot be empty if is_individual_owner is True",
                             "individual_date_of_birth": "This field cannot be empty if is_individual_owner is True",
                             "individual_gender": "This field cannot be empty if is_individual_owner is True",
                             "individual_nationality": "This field cannot be empty if is_individual_owner is True",
                             "individual_occupation": "This field cannot be empty if is_individual_owner is True",
                             "individual_phone_number": "This field cannot be empty if is_individual_owner is True",
                             "individual_email": "This field cannot be empty if is_individual_owner is True",
                             "individual_residential_address": "This field cannot be empty if is_individual_owner is True",
                             "individual_means_of_identification": "This field cannot be empty if is_individual_owner is True"}

            if data.get("individual_surname", None):
                error_message.pop("individual_surname")

            if data.get("individual_first_name", None):
                error_message.pop("individual_first_name")

            if data.get("individual_other_name", None):
                error_message.pop("individual_other_name")

            if data.get("individual_date_of_birth", None):
                error_message.pop("individual_date_of_birth")

            if data.get("individual_date_of_birth", None):
                error_message.pop("individual_date_of_birth")

            if data.get("individual_gender", None):
                error_message.pop("individual_gender")

            if data.get("individual_nationality", None):
                error_message.pop("individual_nationality")

            if data.get("individual_occupation", None):
                error_message.pop("individual_occupation")

            if data.get("individual_phone_number", None):
                error_message.pop("individual_phone_number")

            if data.get("individual_email", None):
                error_message.pop("individual_email")

            if data.get("individual_residential_address", None):
                error_message.pop("individual_residential_address")

            if data.get("individual_means_of_identification", None):
                error_message.pop("individual_means_of_identification")

            raise serializers.DjangoValidationError(
                message=error_message)

        individual_date_of_birth = data.get("individual_date_of_birth", None)
        age = datetime.now().year - individual_date_of_birth.year if individual_date_of_birth else 0
        if individual_date_of_birth and (age < 18 and (not data.get("attestee_surname", None)
                                                       or not data.get("attestee_first_name", None)
                                                       or not data.get("attestee_other_name", None)
                                                       or not data.get("attestee_date_of_birth", None)
                                                       or not data.get("attestee_gender", None)
                                                       or not data.get("attestee_nationality", None)
                                                       or not data.get("attestee_phone_number", None)
                                                       or not data.get("attestee_email", None)
                                                       or not data.get("attestee_residential_address", None)
                                                       or not data.get("attestee_means_of_identification", None)
                                                       or not data.get("attestee_identification_number", None))):
            data["is_attestee"] = True

            error_message = {
                "attestee_surname": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_first_name": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_other_name": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_date_of_birth": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_gender": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_nationality": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_occupation": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_phone_number": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_email": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_residential_address": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee_means_of_identification": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age",
                "attestee__identification_number": "This field is required if the individual_date_of_birth doesn't equates to less than 18 years of age"}

            if data.get("attestee_surname", None):
                error_message.pop("attestee_surname")

            if data.get("attestee_first_name", None):
                error_message.pop("attestee_first_name")

            if data.get("attestee_other_name", None):
                error_message.pop("attestee_other_name")

            if data.get("attestee_date_of_birth", None):
                error_message.pop("attestee_date_of_birth")

            if data.get("attestee_date_of_birth", None):
                error_message.pop("attestee_date_of_birth")

            if data.get("attestee_gender", None):
                error_message.pop("attestee_gender")

            if data.get("attestee_nationality", None):
                error_message.pop("attestee_nationality")

            if data.get("attestee_occupation", None):
                error_message.pop("attestee_occupation")

            if data.get("attestee_phone_number", None):
                error_message.pop("attestee_phone_number")

            if data.get("attestee_email", None):
                error_message.pop("attestee_email")

            if data.get("attestee_residential_address", None):
                error_message.pop("attestee_residential_address")

            if data.get("attestee_means_of_identification", None):
                error_message.pop("attestee_means_of_identification")
            raise serializers.DjangoValidationError(
                message={"attestee_surname": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_first_name": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_other_name": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_date_of_birth": "This filed is required if the individual_date of birth is less than 18",
                         "corporate_gender": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_gender": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_nationality": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_phone_number": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_email": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_residential_address": "This filed is required if the individual_date of birth is less than 18",
                         "attestee_means_of_identification": "This filed is required if the individual_date of birth is less than 18"})

        if not is_corporate_owner and not is_individual_owner:
            raise serializers.DjangoValidationError(
                message={"is_corporate_owner": "cannot be false and is_individual_owner is false",
                         "is_individual_owner": "cannot be false and is_corporate_owner is false"})

        return data

    def create(self, validated_data):
        is_individual_owner = validated_data.get("is_individual_owner", None)
        is_corporate_owner = validated_data.get("is_corporate_owner", None)
        business_name = None

        if is_individual_owner:
            surname = validated_data.pop("individual_surname", None)
            first_name = validated_data.pop("individual_first_name", None)
            other_name = validated_data.pop("individual_other_name", None)
            date_of_birth = validated_data.pop("individual_date_of_birth", None)
            gender = validated_data.pop("individual_gender", None)
            nationality = validated_data.pop("individual_nationality", None)
            occupation = validated_data.pop("individual_occupation", None)
            phone_number = validated_data.pop("individual_phone_number", None)
            email = validated_data.pop("individual_email", None)
            residential_address = validated_data.pop("individual_residential_address", None)
            means_of_identification = validated_data.pop("individual_means_of_identification", None)

            print("I got here.............................................")
            indie = IndividualOwner.objects.create(surname=surname, first_name=first_name, other_name=other_name,
                                                   date_of_birth=date_of_birth, gender=gender, nationality=nationality,
                                                   occupation=occupation, phone_number=phone_number, email=email,
                                                   residential_address=residential_address,
                                                   means_of_identification=means_of_identification)

            pprint(indie)
            # todo: don't forget the photograph, signature and photograph fields
            business_name = BusinessName.objects.create(individual_owner=indie, **validated_data)

        if is_corporate_owner:
            registration_number = validated_data.pop("corporate_registration_number", None)
            name_of_authorized_signatory = validated_data.pop("corporate_name_of_authorized_signatory", None)
            residential_address = validated_data.pop("corporate_residential_address", None)
            gender = validated_data.pop("corporate_gender", None)
            email = validated_data.pop("corporate_email", None)
            phone_number = validated_data.pop("corporate_phone_number", None)
            means_of_identification = validated_data.pop("corporate_means_of_identification", None)

            # identification = validated_data.pop("corporate_identification", None)
            # signature = validated_data.pop("corporate_signature", None)
            # photograph = validated_data.pop("corporate_photograph", None)
            # todo: don't forget the means_of_identification, signature and photograph file fields
            corporate = CorporateOwner(registration_number, name_of_authorized_signatory,
                                       residential_address, gender, email,
                                       phone_number, means_of_identification).save()

            business_name = BusinessName(individual_owner=corporate.pk, **validated_data).save()

        return business_name

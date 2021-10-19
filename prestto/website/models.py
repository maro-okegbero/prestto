from datetime import datetime, timedelta

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt

# Create your models here.
from prestto.settings import SECRET_KEY


class User(AbstractUser):
    """ The general User model """
    first_name = models.CharField(null=True, blank=True, max_length=1000)
    last_name = models.CharField(null=True, blank=True, max_length=1000)
    phone_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    email_authenticated = models.BooleanField(default=False)

    # for partner accounts
    business_name = models.CharField(null=True, blank=True, max_length=1000)
    business_email = models.CharField(null=True, blank=True, max_length=1000)
    is_partner = models.BooleanField(null=True, blank=True, max_length=200, default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)
    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. We're returning the user's fullname
        """
        return f'{self.first_name} {self.last_name}'

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
        }, SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()

    @property
    def private_key(self):
        """
        Key for access
        """
        return self._generate_jwt_token()

    def __str__(self):
        return self.business_name if self.is_partner else self.get_full_name


class ExtraDocument(models.Model):
    """

    """
    document = CloudinaryField('pdf', null=False, blank=False)


class IndividualOwner(models.Model):
    """

    """
    surname = models.CharField(max_length=200, blank=False, null=False)
    first_name = models.CharField(max_length=200, blank=True, null=False)
    other_name = models.CharField(max_length=200, blank=True, null=False)
    date_of_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=100, null=False, blank=False)
    nationality = models.CharField(max_length=100, null=False, blank=False)
    occupation = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=12, null=False, blank=False)  # the phone number
    email = models.EmailField(max_length=12, null=False, blank=False)
    residential_address = models.CharField(max_length=1000, null=False, blank=False)
    means_of_identification = models.CharField(max_length=100, null=False, blank=False)
    identification = CloudinaryField('pdf', null=False, blank=False)
    signature = CloudinaryField('image', null=False, blank=False)
    photograph = CloudinaryField('image', null=False, blank=False)
    other_documents = models.ManyToManyField(ExtraDocument)


class CorporateOwner(models.Model):
    """
    """
    registration_number = models.CharField(max_length=200, blank=False, null=False)
    name_of_authorized_signatory = models.CharField(max_length=200, blank=False, null=False)
    residential_address = models.CharField(max_length=1000, null=False, blank=False)
    gender = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=12, null=False, blank=False)
    phone_number = models.CharField(max_length=12, null=False, blank=False)  # the phone number
    means_of_identification = models.CharField(max_length=100, null=False, blank=False)
    identification = CloudinaryField('pdf', null=False, blank=False)
    signature = CloudinaryField('image', null=False, blank=False)
    photograph = CloudinaryField('image', null=False, blank=False)
    other_documents = models.ManyToManyField(ExtraDocument)


class BusinessName(models.Model):
    """
    BusinessName registration object
    """
    proposed_business_name = models.CharField(max_length=500, null=False,
                                              blank=False)  # the name the business will be called and  registered with legally
    proposed_company_name = models.CharField(max_length=500, null=False,
                                             blank=False)  # the alternative if your proposed business name is unavailable
    business_phone_number = models.CharField(max_length=12, null=False, blank=False)  # the phone number
    business_email = models.EmailField(max_length=12, null=False, blank=False)
    business_address = models.CharField(max_length=1000, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    nature_of_business = models.TextField(max_length=1000, null=False, blank=False)
    business_commencement_date = models.DateField(null=False,
                                                  blank=False)  # cannot be more than 40 days from the date_created
    is_individual_owner = models.BooleanField(null=False, blank=False)
    is_corporate_owner = models.BooleanField(null=False, blank=False)
    individual_owner = models.ForeignKey(IndividualOwner, on_delete=models.CASCADE)
    corporate_owner = models.ForeignKey(CorporateOwner, on_delete=models.CASCADE)

    date_created = models.DateTimeField(default=datetime.now())
    last_created = models.DateTimeField(default=datetime.now())

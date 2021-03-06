"""
utils.py
@Author:    Maro Okegbero
@Date:      OCT 21, 2021
@Time:      3:10 PM
This module contains a number of utility functions useful throughout our application.
No references are made to specific models or views. As a result, they are useful with or
without the application context.
"""
import hashlib
import time
from datetime import datetime
import random
import string

from django.core.mail import send_mail
# from twilio.rest import Client
from prestto import settings

# twilio_client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)


def token_generator(size=5, chars=string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size))


def generate_referral_code(length=7, prefix="BC"):
    """ generate a referral code for users  """

    code = str(int(hashlib.md5(str(token_generator(5)).encode() + str(time.time() * 100).encode()).hexdigest()[:6],
                   16)).zfill(length)
    if prefix:
        code = f"{prefix}{code}"
    return code


def generate_reference_number():
    """
    generates a unique reference number
    """

    year = datetime.now().year.__str__()
    month = datetime.now().month.__str__()
    x = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(9))
    return "-".join(["BC"] + [year] + [month] + ["".join([x])])


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it
    param obj: Object to be populated
    param data: The data to populate it with (dict)
    returns: obj populated with data
    """
    for name, value in data.items():
        if hasattr(obj, name):
            # print(name, value)
            setattr(obj, name, value)

    return obj


# def send_text_message(phone_number, message):
#     """
#     send text message to user
#     """
#     try:
#         text_message = twilio_client.messages.create(
#             body=message,
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=phone_number)
#
#         return text_message
#
#     except Exception as e:
#         print(e, "error............................")
#         return


def send_email_verification_pin(**data):
    """
    send user email
    """

    name = data.get("name")
    email = data.get("email")
    pin = data.get("pin")

    if name and email and pin:
        try:
            print("I'm about to send a mail...............................................")
            send_mail(subject="Email verification",
                      html_message=f"<h1>Hi {name},</h1> <p>Welcome to Prestto. Your verification pin is <b>{pin}</b></p>",
                      message=f"<h1>Hi {name},</h1> <p>Welcome to Prestto. Your verification pin is <b>{pin}</b></p>",
                      from_email="Prestto no-reply@Prestto.com", recipient_list=[f'{email}'], fail_silently=False)
            print("I have  sent the mail...............................................")
            return
        except Exception as e:
            print(e, "Email Error..................................................")
            pass
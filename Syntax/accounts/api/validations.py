import re
from django.core.exceptions import ValidationError


class Validator:

    @staticmethod
    def phone_number(phone_number: str) -> None:
        if not phone_number:
            raise ValidationError('Phone number is required')
        if not re.match(r'^09[0-9]{9}$', phone_number):
            raise ValidationError('Invalid mobile number')
        pass

    @staticmethod
    def validate_email(email: str) -> None:
        if not email:
            raise ValidationError('email address is required')
        if not re.match(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email
        ):
            raise ValidationError('invalid email address')

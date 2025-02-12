# import re
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_integer
#
#
# class Validator:
#
#     @staticmethod
#     def phone_number(phone_number: str) -> None:
#         if not phone_number:
#             raise ValidationError('Phone number is required')
#         if not re.match(r'^09[0-9]{9}$', phone_number):
#             raise ValidationError('Invalid mobile number')

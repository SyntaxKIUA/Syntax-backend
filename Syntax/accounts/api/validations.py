import re
import jdatetime
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError


def validate_jalali_date(value):

    if value:
        try:
            parts = value.split('-')
            if len(parts) != 3:
                raise ValueError("فرمت تاریخ باید 'YYYY-MM-DD' باشد.")

            year, month, day = map(int, parts)
            jdatetime.date(year, month, day)
        except Exception as e:
            raise ValidationError(f"تاریخ جلالی نامعتبر: {value}. {e}")


class ValidatorForgotPassword:
    IRAN_PHONE_REGEX = re.compile(r'^09\d{9}$')

    @staticmethod
    def clean_identifier(value):
        return value.strip()

    @staticmethod
    def get_identifier_field(identifier):
        if ValidatorForgotPassword.IRAN_PHONE_REGEX.match(identifier):
            return "phone_number"
        elif "@" in identifier:
            try:
                validate_email(identifier)
            except DjangoValidationError:
                raise serializers.ValidationError(
                    "Email format is not correct.")
            return "email"
        return False

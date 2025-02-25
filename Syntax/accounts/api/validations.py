from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
import jdatetime


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


def validate_non_empty_password(password):
    if not password:
        raise ValidationError(
            _("Password must not be empty."),
            code="password_empty"
        )

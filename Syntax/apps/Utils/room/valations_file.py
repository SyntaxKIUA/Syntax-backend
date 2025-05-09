from rest_framework.exceptions import ValidationError


def validate_file_size(file):
    max_size = 20 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError("File size must be under 20MB.")
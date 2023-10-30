from django.core.exceptions import ValidationError


def min_value_validator(price):
    """Validates the price of a group"""
    if price <= 0:
        raise ValidationError(message="Narx 0 dan katta qiymat bo'lishi shart")


def subject_name_length_validator(name):
    """Validates the length of a subject name"""
    if len(name) <= 3:
        raise ValidationError(message="Fan nomi eng kamida 4 ta belgi bo'lishi kerak")

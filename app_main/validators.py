from django.core.exceptions import ValidationError


def min_value_validator(price):
    """Validates the price of a group"""
    if price <= 0:
        raise ValidationError(message="Narx 0 dan katta qiymat bo'lishi shart")    
    return True

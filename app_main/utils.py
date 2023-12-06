from django.db.models import Sum
from .models import Payment, Group


def get_months() -> dict:
    months = {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr",
    }
    return months


def get_payment_info(year: int, month: int) -> tuple:
    groups = Group.objects.all()

    total_payment = 0

    total_paid = Payment.objects.filter(month__year__exact=year, month__month__exact=month).aggregate(
        paid_amount=Sum("amount")).get("paid_amount")

    for group in groups:
        total_payment += group.price * group.pupil_set.count()
     
    if not total_paid:
        total_paid = 0

    return total_paid, total_payment

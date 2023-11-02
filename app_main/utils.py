from datetime import date

from django.db.models import Sum
from .models import Payment, Pupil


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


def get_payment_info(year: int = None, month: int = None) -> tuple:
    pupils = Pupil.objects.all()

    if not year:
        year = date.today().year
        month = date.today().month

    total_payment = 0

    total_payment = pupils.filter(created__year__exact=year, created__month__exact=month).aggregate(
        total_payment=Sum("group__price")).get("total_payment")
    total_paid = Payment.objects.filter(month__year__exact=year, month__month__exact=month).aggregate(
        paid_amount=Sum("amount")).get("paid_amount")

    if not total_paid:
        total_paid = 0
    if not total_payment:
        total_payment = 0

    return total_paid, total_payment

from django.db.models import Sum
from .models import Payment, Group, Expense


def get_months() -> dict:
    """Helper function to get month name by month number"""

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
    """Returns payment information for a particular month"""

    groups = Group.objects.all()
    total_payment = 0

    total_paid = Payment.objects.filter(month__year__exact=year, month__month__exact=month).aggregate(
        paid_amount=Sum("amount")
    ).get("paid_amount")

    for group in groups.filter(created__year__lte=year):
        total_payment += group.price * group.pupil_set.count()

    if not total_paid:
        total_paid = 0

    return total_paid, total_payment


def get_total_expenses_amount(year: int, month: int) -> int:
    """Returns total expenses amount for a particular month"""

    expenses = Expense.objects.filter(created__year__exact=year, created__month__exact=month).aggregate(
        total_amount=Sum("amount")
    ).get("total_amount")

    return expenses

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Payment, Group, Expense
from datetime import date

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


def get_total_payment_info_by_groups(year: int, month: int) -> tuple:
    """Returns payments details by groups"""

    day = 31 if month in (1, 3, 5, 7, 8, 10, 12) else 30
    if month == 2:
        day = 28

    requested_date = date(year=year, month=month, day=day)
    groups = Group.objects.filter(created__lte=requested_date)

    payments_dataset_by_groups = []

    for group in groups:
        total_paid = Payment.objects.filter(month__year__exact=year, month__month__exact=month,
                                            group=group).aggregate(paid_amount=Sum("amount")).get("paid_amount")
        total_payment = group.price * group.pupil_set.count()
        payments_dataset_by_groups.append({
            "name": group.name,
            "total_paid": total_paid or 0,
            "total_payment": total_payment or 0
        })

    return payments_dataset_by_groups, groups


def get_expenses_amount(year: int, month: int) -> tuple:
    """Returns expenses list and total expenses amount for a particular month"""

    expenses = Expense.objects.filter(created__year__exact=year, created__month__exact=month).order_by("-created", "-amount")
    expenses_dataset = []

    for expense in expenses:
        expenses_dataset.append({
            "owner": expense.get_owner_fullname,
            "name": expense.name,
            "amount": expense.amount,
            "note": expense.note,
            "date": expense.created.strftime("%d-%m-%Y %H:%M:%S"),
        })

    return expenses_dataset, expenses


def format_number(number):
    if not number:
        return 0
    formatted_number = "{:,}".format(number)
    return formatted_number

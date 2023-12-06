import uuid

from datetime import date

from django.db.models.signals import pre_delete
from django.db import models
from app_users.models import User

from . import validators


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name='Fan nomi', unique=True, validators=[
                            validators.subject_name_length_validator])
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def has_groups(self):
        return self.group_set.all().count() > 0

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    subject = models.ForeignKey(
        to=Subject, on_delete=models.PROTECT, verbose_name='Fan nomi')
    teacher = models.ForeignKey(
        to=User, on_delete=models.PROTECT, verbose_name='O\'qituvchisi')
    name = models.CharField(
        max_length=200, verbose_name='Guruh nomi', unique=True)
    price = models.IntegerField(verbose_name='Guruh to\'lovi', validators=[
                                validators.min_value_validator])
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def has_students(self):
        return self.pupil_set.all().count() > 0

    @property
    def get_total_payment(self):
        return self.pupil_set.count() * self.price
    
    def __str__(self) -> str:
        return self.name


class Pupil(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Ism')
    last_name = models.CharField(max_length=200, verbose_name='Familiya')
    group = models.ForeignKey(
        to=Group, on_delete=models.PROTECT, verbose_name='Guruh')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = (
            ('first_name', 'last_name', 'group'),
        )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def payments(self):
        return self.payment_set.filter(month__month=str(date.today().month))

    @property
    def is_fully_paid(self):
        for payment in self.payment_set.all():
            if payment.month == str(date.today())[:-3] and payment.amount == self.group.price:
                return True
        return False

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Payment(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    owner_fullname = models.CharField(max_length=200, blank=True, null=True)
    month = models.DateField(max_length=200, null=True,
                             verbose_name='To\'lov oyi')
    pupil = models.ForeignKey(
        to=Pupil, on_delete=models.SET_NULL, null=True, verbose_name='O\'quvchi')
    pupil_fullname = models.CharField(max_length=200, blank=True, null=True)
    group = models.ForeignKey(
        to=Group, on_delete=models.SET_NULL, null=True, verbose_name='Guruh')
    group_name = models.CharField(max_length=200, blank=True, null=True)
    amount = models.IntegerField(verbose_name='To\'lov')
    note = models.TextField(
        verbose_name='Eslatma / To\'lov tarifi', blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name='To\'lov vaqti')
    updated = models.DateTimeField(
        auto_now=True, null=True, verbose_name='O\'zgartirilgan vaqt')
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def is_changed(self) -> bool:
        return self.created != self.updated

    def __str__(self) -> str:
        return f'{self.month} - {self.pupil} - {self.amount}' if self.pupil else f'{self.month} - {self.pupil_fullname} - {self.amount}'
    
    class Meta:
        ordering = ('-created', 'amount')

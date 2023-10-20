import uuid

from datetime import date

from django.db import models
from app_users.models import User


# class Subject(models.Model):
#     name = models.CharField(max_length=200, verbose_name='Fan nomi', unique=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#
#     def __str__(self) -> str:
#         return self.name


# class Group(models.Model):
#     subject = models.ForeignKey(to=Subject, on_delete=models.SET_NULL, null=True, verbose_name='Fan nomi')
#     teacher = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name='O\'qituvchisi')
#     name = models.CharField(max_length=200, verbose_name='Guruh nomi', unique=True)
#     price = models.IntegerField(default=0, verbose_name='Guruh to\'lovi')
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#
#     def __str__(self) -> str:
#         return self.name


# class Pupil(models.Model):
#     first_name = models.CharField(max_length=200, verbose_name='Ism', null=True)
#     last_name = models.CharField(max_length=200, verbose_name='Familiya', null=True)
#     fullname = models.CharField(max_length=200, verbose_name='To\'liq Ism va Familiya', null=True)
#     group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)
#     created = models.DateTimeField(auto_now_add=True, null=True)
#     updated = models.DateTimeField(auto_now=True, null=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#
#     @property
#     def payments(self):
#         return self.payment_set.filter(month=str(date.today())[:-3])
#
#     class Meta:
#         unique_together = (
#             ('fullname', 'group'),
#         )
#
#     def __str__(self) -> str:
#         return f'{self.first_name} {self.last_name}'
#
#     @property
#     def is_fully_paid(self):
#         for payment in self.payment_set.all():
#             if payment.month == str(date.today())[:-3] and payment.amount == self.group.price:
#                 return True
#         return False


# class Payment(models.Model):
#     owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
#     month = models.CharField(max_length=200, null=True)
#     pupil = models.ForeignKey(to=Pupil, on_delete=models.SET_NULL, null=True)
#     group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)
#     amount = models.IntegerField(verbose_name='To\'lov')
#     note = models.TextField(verbose_name='Eslatma / To\'lov tarifi')
#     created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='To\'lov vaqti')
#     updated = models.DateTimeField(auto_now=True, null=True, verbose_name='O\'zgartirilgan vaqt')
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # @property
    # def is_changed(self) -> bool:
    #     return self.created != self.updated
    #
    # def __str__(self) -> str:
    #     return f'{self.pupil} - {self.amount}'

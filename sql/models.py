from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = None
    is_staff = None
    is_superuser = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Expense(models.Model):
    EXPENSE_TYPES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=EXPENSE_TYPES)
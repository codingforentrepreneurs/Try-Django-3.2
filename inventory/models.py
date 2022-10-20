from django.conf import settings
from django.db import models
from meals.signals import (
    meal_added,
    meal_removed
)
from meals.utils import generate_meal_queue_totals

User = settings.AUTH_USER_MODEL

class InventoryRequestStatus(models.TextChoices):
    REQUESTED = 'r', 'Requested'
    PURCHASED = 'p', 'Purchased'
    STOCKED = 's', 'In Stock'
    UNAVAILABLE = 'u', 'Unavailable'
    DECLINED = 'd', 'Declined'
    ARCHIVED = 'a', 'Archive'


class InventoryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    unit = models.CharField(max_length=50, blank=True, null=True)
    total = models.DecimalField(decimal_places=4, max_digits=20, blank=True, null=True)
    status = models.CharField(max_length=1, choices=InventoryRequestStatus.choices, default=InventoryRequestStatus.REQUESTED)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


def meal_added_reciever(sender, instance, *args, **kwargs):
    user = instance.user
    qs = InventoryRequest.objects.filter(user=user, status=InventoryRequestStatus.REQUESTED)
    if qs.exists():
        qs.update(status=InventoryRequestStatus.ARCHIVED)
    data = generate_meal_queue_totals(user)
    data = [InventoryRequest(**{'user': user, **x}) for x in data]
    InventoryRequest.objects.bulk_create(data)

meal_added.connect(meal_added_reciever)
meal_removed.connect(meal_added_reciever)
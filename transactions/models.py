from django.db import models
import uuid
from authapi.models import Customer

# Create your models here.
class Transaction(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    sender = models.ForeignKey(Customer, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Customer, related_name="receiver", on_delete=models.CASCADE)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
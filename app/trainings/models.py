import uuid

from django.db import models
from dictionary.models import UserProfile, Card


# Create your models here.
class CardTraining(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=False, null=False)
    answer = models.CharField(max_length=150)
    onetime = models.BooleanField(default=True)

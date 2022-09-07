import uuid

from django.db import models
from django.contrib.auth.models import User

class BootToken(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='BootTokens')

class BootSignal(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    type = models.CharField(max_length=20)
    token = models.ForeignKey(BootToken, default=None, null=True, on_delete=models.CASCADE, related_name="BootSignals")

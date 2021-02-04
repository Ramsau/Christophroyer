from django.db import models

class BootSignal(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    type = models.CharField(max_length=20)

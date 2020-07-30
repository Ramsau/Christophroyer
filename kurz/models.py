from django.db import models

import uuid

class Clip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('created', ), )

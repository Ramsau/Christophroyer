from django.db import models

import uuid

class Clip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now=True)
    accessed = models.IntegerField(default=1)

class MissingWord(models.Model):
    word = models.CharField(primary_key=True, max_length=255)
    accessed = models.IntegerField(default=1)


from django.db import models
from user.models.user import User
from core.models import AbstractModel


class APIKey(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    api_key_harsh = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

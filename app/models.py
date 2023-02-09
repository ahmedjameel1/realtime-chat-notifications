from django.db import models
from accounts.models import Account

# Create your models here.


class Notification(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.text

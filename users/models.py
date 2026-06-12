from django.db import models
from django.contrib.auth.models import User

class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=6)

    def __str__(self):
        return f"Code for {self.user.username}: {self.code}"
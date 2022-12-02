from django.db import models

class Email(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
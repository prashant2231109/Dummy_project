from django.contrib.auth.models import User
from django.db import models

from company.models import Company


class Subscriber(models.Model):
    """Model representing one user has one subscriber profile which is linked to a company.
    
    Each subscriber is associated with one company, and each company can have
    multiple subscribers."""
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_subscribers"
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

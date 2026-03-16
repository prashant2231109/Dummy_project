from django.contrib.auth.models import User
from django.db import models



class Company(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,
        related_name="company_created",
    )
    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,
        related_name="company_updated",
    )
    
    name = models.CharField(max_length=100, db_index=True)
    url = models.URLField(max_length=500, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "url")

    def __str__(self):
        return self.name


class Subscriber(models.Model):
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

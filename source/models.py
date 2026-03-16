from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from clients.models import Company


class Source(models.Model):
    tagged_companies = models.ManyToManyField(
        Company, related_name="tagged_sources"
    )

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_sources"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="source_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="source_updated"
    )

    name = models.CharField(max_length=500, db_index=True)
    url = models.URLField(max_length=1000)

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("url", "company")

    def __str__(self):
        return self.name

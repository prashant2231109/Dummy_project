from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from company.models import Company


class Source(models.Model):
    """
    Model representing a news source that can be associated with company
    and tagged with multiple companies.
    Each source has unique url and company combination
    """

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

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=1000)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("url", "company")

        indexes = [
            GinIndex(
                fields=["name"],
                name="source_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Company(models.Model):
    """Model representing a company that can be tagged in sources
    and stories.
    each company can unique name and url combination.
    """

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="company_created",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="company_updated",
    )

    name = models.CharField(max_length=256)
    url = models.URLField(max_length=500, unique=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:

        indexes = [
            GinIndex(
                fields=["name"],
                name="company_name_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.name

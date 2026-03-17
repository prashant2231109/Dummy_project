from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.db import models


from company.models import Company
from source.models import Source


class Story(models.Model):
    tagged_companies = models.ManyToManyField(
        Company, related_name="tagged_stories"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_stories",
        default=""
    )
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name="source_stories"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="story_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="story_updated"
    )

    title = models.CharField(max_length=500)
    url = models.URLField(max_length=1500)
    body_text = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.source:
            self.tagged_companies.set(self.source.tagged_companies.all())

    class Meta:
        ordering = ["created_on"]
        unique_together = ("url", "company")
        indexes = [
            GinIndex(
                fields=["body_text"],
                name="story_body_text_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["title"],
                name="story_title_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.source.name}"

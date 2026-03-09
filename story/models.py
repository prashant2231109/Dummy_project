from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from clients.models import Company
from source.models import Source


class Story(models.Model):
    tagged_companies = models.ManyToManyField(
        Company, related_name="tagged_stories"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_stories",
        default=None,
        null=True,
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

    title = models.CharField(max_length=200, db_index=True)
    url = models.URLField(max_length=500)
    body_text = models.TextField()
 
  
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("url", "company")

    def __str__(self):
        return f"{self.title} - {self.source.name}"
    
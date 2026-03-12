from django.contrib import admin

from source.models import Source

# Register your models here.

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    ordering = ["created_on"]
    list_display = (
        "id",
        "name",
        "url",
        "company",
        "created_by",
        "updated_by",
        "created_on",
        "updated_on",
    )
    search_fields = ["name", "company__name"]
    list_filter = ["created_on", "updated_on", "company__name"]
    
from django.contrib import admin

from company.models import Company

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "url",
        "created_by",
        "updated_by",
        "created_on",
        "updated_on",
    )
    search_fields = ["name"]
    list_filter = ["created_on", "updated_on"]

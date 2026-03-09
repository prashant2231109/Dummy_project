from django.contrib import admin
from clients.models import Company, Subscriber
from source.models import Source
from story.models import Story


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


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "company", "created_on", "updated_on")
    search_fields = ["user__username", "company__name"]

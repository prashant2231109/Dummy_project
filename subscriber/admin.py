from django.contrib import admin

from subscriber.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "company", "created_on", "updated_on")
    search_fields = ["user__username", "company__name"]

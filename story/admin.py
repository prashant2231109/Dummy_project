from django.contrib import admin

from story.models import Story

# Register your models here.
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    ordering = ["created_on"]
    list_display = (
        "id",
        "title",
        "source",
        "url",
        "company",
        "created_by",
        "updated_by",
        "created_on",
        "updated_on",
    )
    
    search_fields = ["title", "source__name"]
    list_filter = ["created_on", "updated_on", "company"]
    
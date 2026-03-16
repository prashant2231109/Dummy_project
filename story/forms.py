from django import forms
from django.core.exceptions import ValidationError
from dal import autocomplete

from story.models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["title", "url", "source", "body_text", "tagged_companies"]
        widgets = {
            "tagged_companies": autocomplete.ModelSelect2Multiple(
                url="story:company-autocomplete"
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        company = self.request.user.subscriber.company
        if (
            Story.objects.select_related("company")
            .filter(url=url, company=company)
            .exists()
        ):
            raise ValidationError(
                "Story with this URL already exists for your company."
            )
        return cleaned_data

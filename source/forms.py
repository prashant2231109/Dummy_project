from django.core.exceptions import ValidationError
from django import forms

from source.models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["name", "url", "tagged_companies"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get("url")
        company = self.request.user.subscriber.company
        if Source.objects.filter(url=url, company=company).exists():
            raise ValidationError(
                "Source with this URL already exists for your company."
            )
        return cleaned_data

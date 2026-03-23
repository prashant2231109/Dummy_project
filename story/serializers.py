from rest_framework import serializers

from company.models import Company
from story.models import Story
from source.serializers import SourceSerializer




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]

       


class StorySerializer(serializers.ModelSerializer):
    tagged_companies= serializers.PrimaryKeyRelatedField(
        many=True, queryset=Company.objects.only("id") 
    )
    tagged_companies_data = CompanySerializer(
        many=True, read_only=True, source="tagged_companies"
    )
    source_data = SourceSerializer(read_only=True , source="source")

    company_data = CompanySerializer(read_only=True, source="company")

    class Meta:
        model = Story
        fields = [
            "id",
            "title",
            "url",
            "body_text",
            "source",
            "source_data",
            "company_data",
            "tagged_companies",
            "tagged_companies_data",
        ]
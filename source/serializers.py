from rest_framework import serializers

from company.models import Company
from source.models import Source


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class SourceSerializer(serializers.ModelSerializer):
    tagged_companies = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Company.objects.all()
    )

    tagged_companies_data = CompanySerializer(
        many=True, read_only=True, source="tagged_companies"
    )

    class Meta:
        model = Source
        fields = [
            "id",
            "name",
            "url",
            "tagged_companies",
            "tagged_companies_data",
        ]

  
        

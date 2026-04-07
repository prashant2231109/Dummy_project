from rest_framework import serializers

from company.models import Company
from source.models import Source


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]


class SourceSerializer(serializers.ModelSerializer):
    tagged_companies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Company.objects.all(),
        write_only=True,
    )

    tagged_companies_data = CompanySerializer(
        many=True, read_only=True, source="tagged_companies"
    )

    is_owner = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = Source
        fields = [
            "id",
            "name",
            "url",
            "tagged_companies",
            "tagged_companies_data",
            "is_owner",
            "is_staff",
        ]

    def get_is_owner(self, obj):
        return obj.created_by_id == self.context["request"].user.id
    
    def get_is_staff(self, obj):
        return self.context["request"].user.is_staff

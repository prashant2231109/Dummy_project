from rest_framework import serializers

from company.models import Company
from story.models import Story
from source.serializers import SourceSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name"]

       
class StorySerializer(serializers.ModelSerializer):
    tagged_companies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Company.objects.all(),
        write_only=True  
    )
    tagged_companies_data = CompanySerializer(
        many=True, read_only=True, source="tagged_companies"
    )
    source_data = SourceSerializer(read_only=True, source="source")
    company_data = CompanySerializer(read_only=True, source="company")

    is_owner = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()

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
            "is_owner",
            "is_staff"
            
        ]
    def get_is_owner(self, obj):
        return obj.created_by_id == self.context["request"].user.id
    
    def get_is_staff(self, obj):
        return self.context["request"].user.is_staff   
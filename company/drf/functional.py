from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from company.serializers import CompanySerializer

from company.models import Company



@api_view(["GET"])
def company_view(request):
    company=Company.objects.all()
    serializer = CompanySerializer(company, many=True)
    return Response(serializer.data)
    


        

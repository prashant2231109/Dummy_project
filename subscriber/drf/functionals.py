from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from subscriber.serializers import SignupSerializer , LoginSerializer
from django.views.decorators.csrf import csrf_exempt

from source.models import Source
from django.contrib.auth import login

from rest_framework_simplejwt.tokens import RefreshToken



@csrf_exempt
@api_view(["POST"])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "username": user.username
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]

      
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Login successful",
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
             
        })

        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
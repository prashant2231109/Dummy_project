from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscriber.serializers import LoginSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            return Response({
                "message": "Login successful",
                "username": user.username
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
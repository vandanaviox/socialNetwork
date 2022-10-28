from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializer import RegisterSerializer, LoginSerializer
from rest_framework import status
from account.utils import exception_handling
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(APIView):

    @exception_handling
    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'Data': {},
                    'Message': serializer.errors,
                    'Status': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response({

            'Data': serializer.data,
            'Message': 'Your account is created',
            'Status': True
        }, status= status.HTTP_201_CREATED)


class LoginView(APIView):

    @exception_handling
    def post(self, request):
        
        serializer=LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'Data': {},
                'Message': serializer.errors,
                'Status': False
            }, status=status.HTTP_400_BAD_REQUEST)

        response = serializer.get_jwt_token(serializer.data)
        return Response(response, status=status.HTTP_200_OK)
    

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classess = [JWTAuthentication]
    
    @exception_handling
    def get(self, request):
        logout(request)
        return Response({
            'data': {},
            'message': "User Logged Out Successfully",
            'status': True
        }, status = status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import status
from django.contrib.auth import authenticate
from .models import BlacklistedToken
from .decorators import jwt_required

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create JWT manually
        payload = {
            'id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=1)  # token valid 1 hour
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token})

class LogoutView(APIView):

    @jwt_required
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]

        # Save token to blacklist
        BlacklistedToken.objects.create(token=token)

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
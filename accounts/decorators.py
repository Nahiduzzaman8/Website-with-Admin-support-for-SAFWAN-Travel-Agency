import jwt
from functools import wraps
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import User, BlacklistedToken

def jwt_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization header missing or invalid'}, status=401)
        
        token = auth_header.split(' ')[1]

        # Check blacklist
        if BlacklistedToken.objects.filter(token=token).exists():
            return Response({'error': 'Token has been logged out'}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
            request.user = user
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=401)

        return func(self, request, *args, **kwargs)
    
    return wrapper
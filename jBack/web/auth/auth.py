
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        is_admin = user.is_staff
        return Response({
            'token': token.key,
            'id': user.id,
            'user_type': 'admin' if is_admin else 'user'
        })
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please Enter Username and Password'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    Token.objects.create(user=user)
    return Response({'message': 'Created! '}, status=status.HTTP_201_CREATED)

from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.http import JsonResponse
from .middleware import check_permission

def ping(request):
    return JsonResponse({'ping': 'pong'})

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def register(request):
    data = request.data
    if User.objects.filter(username=data['username']).exists():
        return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create(
        username=data['username'],
        password=make_password(data['password']),
    )
    admin_group, _ = Group.objects.get_or_create(name='admin')
    user.groups.add(admin_group)
    user.save()
    return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is None:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    tokens = get_tokens_for_user(user)
    return Response({'token': tokens['access']})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'groups': [group.name for group in user.groups.all()],
    })

# Permission-protected views using the custom check_permission decorator
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@check_permission(['admin_permission'])
def admin_permission(request):
    return Response({'message': 'Admin permission granted'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@check_permission(['standard_permission'])
def standard_permission(request):
    return Response({'message': 'Standard permission granted'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@check_permission(['standard_permission', 'admin_permission'])
def admin_standard_permission(request):
    return Response({'message': 'Admin and Standard permission granted'})

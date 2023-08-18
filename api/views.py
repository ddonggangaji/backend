from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import *
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter

from api.models import *
from api.serializers import *


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    user_name = request.data.get('user_name')
    password = request.data.get('password')

    serializer = SignupSerializer(data=request.data)
    serializer.user_name = user_name
    serializer.password = password

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user_name = request.data.get('user_name')
    password = request.data.get('password')

    user = authenticate(user_name=user_name, password=password)
    if user is None:
        return Response({'message': '아이디 또는 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    update_last_login(None, user)

    return Response({'refresh_token': str(refresh),
                     'access_token': str(refresh.access_token), }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def id_check(request):
    user_name = request.data.get('user_name')

    try:
        user = User.objects.get(user_name=user_name)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': '해당 유저가 존재하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserinfoViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes([AllowAny])
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_name', 'phone_number', 'nick_name', 'role']


@api_view(['PATCH'])
@permission_classes([AllowAny])
def change_password(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    re_password = request.data.get('re_password')

    try:
        if password == re_password:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(password)
            user.save()
            return Response({'message': '비밀번호 변경이 완료되었습니다.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': '비밀번호가 서로 같지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes([AllowAny])
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'user', 'title', 'helper_phone_number', "helped_phone_number", "status"]


class UserReviewViewSet(viewsets.ModelViewSet):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer
    permission_classes([AllowAny])
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'service', 'review', 'score']

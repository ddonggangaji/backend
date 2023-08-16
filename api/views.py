from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import *
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

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
def user_info(request):
    phone_number = request.data.get('phone_number')

    try:
        user = User.objects.get(phone_number=phone_number)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': '해당 유저가 존재하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


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


@api_view(['GET', "POST"])
@permission_classes([AllowAny])
def service(request):
    if request.method == 'GET':

        user = request.GET.get('user', None)
        category = request.GET.get('category', None)
        title = request.GET.get('title', None)
        helper_phone_number = request.GET.get('helper_phone_number', None)
        helped_phone_number = request.GET.get('helped_phone_number', None)

        service = Service.objects.filter(helper_phone_number=helper_phone_number,
                                         helped_phone_number=helped_phone_number,
                                         category=category,
                                         title=title,
                                         user=user)

        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', "POST"])
@permission_classes([AllowAny])
def category(request):
    if request.method == "GET":
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

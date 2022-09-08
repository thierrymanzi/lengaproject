# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:20:54
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-05-27 13:56:36
# Project: lenga

from django.contrib.auth import authenticate
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.models import Partner, Location
from users.api.filters import UserFilter
from users.api.serializers import (
    PermissionsViewSerializer, UserRegistrationSerializer,
    PartnerSerializer, LocationSerializer)
from users.api.serializers import (
    UserSerializer, LoginSerializer, UserExportSerializer
)
from users.models import Permissions
from users.models import User
from utils import view_mixins as generics
from utils.common import FileExport


class ListCreatePermissions(generics.ListCreateAPIView):
    """
    Permissions can be viewed/listed and
    new permissions can also be created on neeed basis
    """
    queryset = Permissions.objects.all()
    serializer_class = PermissionsViewSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        perms = request.data
        if isinstance(perms, dict):
            return super().create(request, *args, **kwargs)
        else:
            permissions = []
            for perm in perms:
                permission = Permissions(
                    name=perm.get('name'),
                    description=perm.get('description')
                )
                permissions.append(permission)

            Permissions.objects.bulk_create(permissions)

            return Response({'success': 'Permissions created successfully'},
                            status=status.HTTP_201_CREATED)


class UpdatePermissionsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Existing permissions can be altered
    either by being updated or deleted by user/admin
    """
    queryset = Permissions.objects.all()
    serializer_class = PermissionsViewSerializer
    lookup_field = 'id'


class ListUsers(generics.ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.filter(is_active=True)
    filter_class = UserFilter
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except KeyError as e:
            return Response({'Error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def perform_create(self, serializer):
        passwd = self.request.data.get('password')

        if not passwd:
            raise KeyError('Password not provided')
        user = serializer.save()
        user.set_password(passwd)
        user.save()

class ListPartners(generics.ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Partner.objects.filter(is_active=True).exclude(name__icontains='test')
    serializer_class = PartnerSerializer


class ListLocations(generics.ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Location.objects.filter(is_active=True).exclude(name__icontains='test')
    serializer_class = LocationSerializer


class RetrieveUpdateUsers(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'

    @transaction.atomic
    def perform_update(self, serializer):
        perm = self.request.data.get('permission')
        user = serializer.save()

        if perm:
            user.permission.add(perm)


class CurrentUserView(APIView):
    """
    Current user
    """
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [OAuth2Authentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        """
        Get currently logged in user from frontend
        """

        return Response(UserSerializer(request.user).data)


@method_decorator(csrf_exempt, name="dispatch")
class LoginUserView(generics.CreateAPIView):
    """
    Check user exists
    """
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginSerializer
    model = User

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        self.user = None

        # str_user_password = User.objects.make_random_password()

        if serializer.is_valid():
            # if passed relevant details

            self.username = serializer.data.get("username")
            self.password = serializer.data.get("password")
            user = authenticate(
                username=self.username,
                password=self.password
            )

            if user:
                # means user has been logged in successfully
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid login details provided'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class UserRegistration(generics.CreateAPIView):
    """
    Check user exists
    """
    permission_classes = []
    authentication_classes = []
    serializer_class = UserRegistrationSerializer
    model = User

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        # update user password
        user.set_password(request.data['password'])
        user.save()

        headers = self.get_success_headers(serializer.data)

        return Response(UserSerializer(user).data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class ExportUsers(generics.ListAPIView):
    filter_class = UserFilter


    def get(self, request, *args, **kwargs):
        serializer = UserExportSerializer(
            self.filter_queryset(User.objects.filter(is_staff=True)), many=True)
        handler = FileExport(serializer.data)
        return Response({'file_url': handler.file_export()})

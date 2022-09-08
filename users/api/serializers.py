# -*- coding: utf-8 -*-
# @Author: Simon Muthusi
# @Email: simonmuthusi@gmail.com
# @Date:   2020-05-27 11:20:33
# @Last Modified by:   Simon Muthusi
# @Last Modified time: 2020-06-12 08:19:13
# Project: lenga
from tkinter import E
from rest_framework import serializers

from learning.models import Location, Partner
from users.models import Permissions, User


class PermissionsViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permissions
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    all_permissions = serializers.ReadOnlyField()
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'groups', 'is_superuser',
            'user_permissions', 'permission',
        )

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        exclude = (
            'is_active',
        )


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = (
            'is_active',
        )



class UserExportSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'account_type', 'location')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    location = serializers.CharField(required=False, max_length=100, allow_blank=True)
    partner = serializers.CharField(required=False, max_length=100, allow_blank=True)
    signup_date = serializers.CharField(required=False, max_length=100, allow_blank=True)

    class Meta:
        model = User
        exclude = (
            'last_login', 'groups', 'is_superuser',
            'user_permissions', 'permission', 'is_active', 'fcm_key',
            'is_staff'
        )

    def create(self, validated_data):

        try:
          
            loc = validated_data['location']
            location = Location.objects.get_or_create(name=loc.strip())[0]
            #location = Location.objects.create(name=loc.strip())[0]
            #validated_data['location'] = location
  
            if location:
             validated_data.get['location']=location


        except Exception as e:
            print("Location error:{}".format(e))
       

        try:
            part = validated_data['partner']
            partner = Partner.objects.filter(name=part.strip())
            if partner:
                partner = partner.first()
            else:
                partner = Partner.objects.create(name=part.strip())
            validated_data.get['partner'] = partner
        except Exception as e:
            pass

        try:
            validated_data['signup_date'] = validated_data.get['signup_date']
        except Exception as e:
            print("Partner error:{}".format(e))

        return super(UserRegistrationSerializer, self).create(validated_data)






class LoginSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

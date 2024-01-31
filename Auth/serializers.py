from rest_framework import serializers
from .models import (User  ,)
from django.contrib.auth import authenticate
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError , AccessToken
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import smart_str , force_bytes , DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import *
from django.contrib.auth.models import Group
from xml.dom import ValidationErr

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ('email', 'username','password','is_mmrda' , 'is_kfw' , 'is_contractor' , 'is_consultant' , 'is_RNR')

    def validate(self, data):
        username = data.get('username')
        if username == "" or username == None:
            raise serializers.ValidationError('Username can not be empty')
        if username[0].islower():
            raise serializers.ValidationError('Username First letter must be uppercase')
        return data


    def create(self,validated_data):
        return User.objects.create_user(**validated_data)



class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ("email", "password")

        extra_kwargs ={'password':{'write_only':False}}

class NewLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    groupName = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("email", "password","groupName")

        extra_kwargs ={'password':{'write_only':False}}
        
    
    def validate(self, data):
        email = data.get('email')
        groupName = data.get('groupName')
        password = data.get('password')

        # Check if the user with the specified email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        # Check if the group with the specified name exists
        try:
            group = Group.objects.get(name=groupName)
        except Group.DoesNotExist:
            raise serializers.ValidationError("Group does not exist.")

        # Additional validation based on your requirements
        if not user.groups.filter(name=groupName).exists():
            raise serializers.ValidationError("User is not a member of the specified group.")

        if not authenticate(email=email, password=password):
            raise serializers.ValidationError("Invalid Credentials.")

        # You can perform other additional validation logic here
        # For example, check if the user has specific attributes or conditions

        return data
      
class ChangePasswordSerializer(serializers.Serializer):
   password = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only =True)
   class Meta:
    Feilds = ["password"]
   
   def validate(self, data):
    password = data.get('password')
    user = self.context.get('user')
    user.set_password(password)
    user.save()
    return data


# The `PasswordResetEmailSerializer` class is used to serialize and validate the email field for
# sending a password reset email to a registered user.
class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 255)
    class Meta:
        fileds = ['email']


    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email ).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded ID" , uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password reset Token" , token)
            link = 'http://localhost:3000/api/auth/reset/'+ uid+'/'+token
            print("password Rest link" , link)
            
            body = 'click following link to reset your Password : ' + link  
            data = {
                'subject' : 'Reset Your Password ',
                'body' : body,
                'to_email':user.email
            }
            Util.send_email(data)

        else:
            raise ValidationErr("You are not a registered user")
        return data

class PasswordRestSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255 , style={'input_type':'password'}, write_only =True)
    class Meta:
        Feilds = ["password"]
   
    def validate(self, data):
        try:
            password = data.get('password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if data["password"] == "" or data["password"] == None:
                raise serializers.ValidationError("password cannot be empty")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id =id)
            if not PasswordResetTokenGenerator().check_token(user , token):
                raise ValidationErr("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user , token)
            raise ValidationErr("Token is not Valid or Expired")




class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid'),
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            self.fail('bad_token')

        


        


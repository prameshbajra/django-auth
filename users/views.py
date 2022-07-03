
import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy import re

from .authentication import create_access_token, decode_token, refresh_access_token
from .models import User
from .serializers import UserSerializer


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User does not exist.')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password. Please try again.')

        access_token = create_access_token(id = user.id)
        refresh_token = refresh_access_token(id = user.id)

        response =  Response({
            'token': access_token
        })
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response



class UserView(APIView):

    def get(self, request):
        auth = get_authorization_header(request=request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_token(type='access_secret', token=token)
            user = User.objects.filter(pk=id).first()
            return Response(UserSerializer(user).data)
        raise AuthenticationFailed('Not authorised to perform the action.')
        

class RefreshTokenView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_token(type='refresh_secret', token=refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutView(APIView):
    
    def post(self, request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.data = {
            'message': 'Successfully Logged Out.'
        }
        return response


























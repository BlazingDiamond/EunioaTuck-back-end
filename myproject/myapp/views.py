# myapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import UserProfile, Post
from .serializers import (
    UserProfileSerializer,
    PostSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from .models import Product
from myapp import serializers
from myapp import models
from django.shortcuts import render
from django.http import HttpResponse


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class UserProfileListCreate(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    def get_all_products(request):
        all_products = Product.objects.all()

        context = {"products": all_products}
        return Response(request, "your_template.html", context)


class ProductsListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]


class ProductImageView(generics.ListAPIView):
    queryset = models.Product.objects.exclude(image="")
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [AllowAny]

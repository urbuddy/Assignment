from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, Purchase, User
from .serializers import ProductSerializer, PurchaseSerializer
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
          'refresh': str(refresh),
          'access': str(refresh.access_token),
    }


def index(request):
    return HttpResponse("Welcome to Application")


class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "User Already Exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            token = get_tokens_for_user(user)
            return Response({"msg": "User Register Successfully", "token": token, "username": username}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        request.session['username'] = username
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'Login Successful', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Username or password is not valid'}, status=status.HTTP_404_NOT_FOUND)


class ProductSellView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.session['username'])
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'image': request.data.get('image'),
            'seller': user.id
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Now product is on sell.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(id=id)
        user = User.objects.get(username=request.session['username'])
        data = {
            'product': product.id,
            'seller': product.seller.id,
            'buyer': user.id,
            'purchase_price': product.price
        }
        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'Product Purchased.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Product, Add_on, Order, OrderItem, PasswordResetRequest
from .serializers import (
    CustomUserSerializer, ProductSerializer, AddOnSerializer,
    OrderSerializer, OrderItemSerializer, PasswordResetRequestSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_password_reset(request):
    username = request.data.get('username') or request.data.get('identifier')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not username:
        return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password or not confirm_password:
        return Response({'error': 'Please provide and confirm your new password.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(username=username.strip()).first()
    if not user:
        return Response({'error': 'User not found with that username.'}, status=status.HTTP_404_NOT_FOUND)

    # Create the password reset request linked to the user with the hashed new password
    PasswordResetRequest.objects.create(
        user=user,
        new_password=make_password(new_password),
        is_approved=False
    )

    return Response({'message': 'Password reset request submitted successfully.'}, status=status.HTTP_201_CREATED)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class AddOnViewSet(viewsets.ModelViewSet):
    queryset = Add_on.objects.all()
    serializer_class = AddOnSerializer
    permission_classes = [permissions.AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param and status_param != 'All':
            queryset = queryset.filter(status=status_param)
        return queryset

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class PasswordResetRequestViewSet(viewsets.ModelViewSet):
    queryset = PasswordResetRequest.objects.all().order_by('-requested_at')
    serializer_class = PasswordResetRequestSerializer
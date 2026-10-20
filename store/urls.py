from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'add-ons', views.AddOnViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'password-resets', views.PasswordResetRequestViewSet)

urlpatterns = [
    path('password-resets/submit/', views.submit_password_reset, name='submit_password_reset'),

    # Standard router URLs
    path('', include(router.urls)),
]
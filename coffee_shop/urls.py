from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/password-resets/', views.submit_password_reset, name='request_password_reset'),
    path('api/request-password-reset/', views.submit_password_reset, name='request_password_reset_alt'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
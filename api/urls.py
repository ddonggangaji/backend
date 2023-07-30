from django.urls import path, include
from rest_framework import routers

from api.views import ProfileViewSet, ServiceViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'service', ServiceViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

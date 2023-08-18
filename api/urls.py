from django.urls import path, include
from api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user_info', UserinfoViewSet, basename='user_info')
router.register('service', ServiceViewSet, basename='service')
router.register('user_review', UserReviewViewSet, basename='user_review')


urlpatterns = [
    # User
    path('', include(router.urls)),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('id_check/', id_check, name='id_check'),
    path("change_password/", change_password, name="change_password"),
    # path("user_img/", user_img, name="user_img"),

]

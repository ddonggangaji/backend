from django.urls import path
from api.views import *

urlpatterns = [
    # User
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('id_check/', id_check, name='id_check'),
    path("user_info/", user_info, name="user_info"),
    path("change_password/", change_password, name="change_password"),

    # Service
    path("service/", service, name="service"),

    # Category
    path("category/", category, name="category"),

]

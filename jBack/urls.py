"""
URL configuration for jBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from jBack.web.auth import auth
from jBack.web.view.meeting_room_view import RoomDetailView, RoomListView
from jBack.web.view import booking_room_view

urlpatterns = [
    
    #Auth
    path("admin/", admin.site.urls),
    path('api/token', obtain_auth_token, name='api_token_auth'),
    path('api/login', auth.login_user, name='login_user'),
    path('api/create_user', auth.create_user, name='create_user'),
    
    #Admin
    path('api/rooms', RoomListView.as_view(), name='room_list'),
    path('api/rooms/<int:pk>', RoomDetailView.as_view(), name='room_detail'),
    
    #User
    path('api/availablerooms', booking_room_view.available_rooms, name='room_list'),
]
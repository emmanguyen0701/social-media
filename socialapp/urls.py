from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views
from . import api

app_name = 'socialapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile_list/', login_required(login_url='/account/login')(views.ProfileList.as_view()), name='profile_list'),
    path('profile_detail/<int:pk>', views.profile_detail, name='profile_detail'),
    path('profile_detail/<int:pk>/image_gallery', views.image_gallery, name='image_gallery'),
    path('account/', include('django.contrib.auth.urls')),
    path('account/register', views.register, name='register'),
    path('api/image', api.ImageDetail.as_view(), name='image_api'),
    path('api/images/<int:pk>', api.ImageList.as_view(), name='images_api'),
    path('chat/', views.chatIndex, name='chat_index'),
    path('chat/<str:room_name>/', views.chatRoom, name='chat_room')
] 
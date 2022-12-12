from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('roommate_feed', views.roommate_feed, name='roommate_feed'),
    path('roommate_upload', views.roommate_upload, name='roommate_upload'),
    path('delete_comm_post/<str:pk>', views.delete_comm_post, name='delete_comm_post'),
    path('delete_room_post/<str:pk>', views.delete_room_post, name='delete_room_post'),

]


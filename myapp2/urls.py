from django.urls import path
from . import views

urlpatterns = [
    path('customsignup-avface/', views.admin_signup, name='admin_signup'),
    path('customlogin-avface/', views.admin_login, name='admin_login'),
    path('customlogout/', views.admin_logout, name='admin_logout'),

    path('custom-avface/', views.custom_panel, name='custom_panel'),

    path('custom-avface/add-category/', views.add_category, name='add_category'),
    path('custom-avface/add-style/', views.add_style, name='add_style'),
    path('custom-avface/add-teacher/', views.add_teacher, name='add_teacher'),
    path('custom-avface/add-video/', views.add_video, name='add_video'),
    path('custom-avface/videos/', views.video_list, name='video_list'),
    path('custom-avface/videos/edit/<int:id>/', views.edit_video, name='edit_video'),
    path('custom-avface/videos/delete/<int:id>/', views.delete_video, name='delete_video'),
]
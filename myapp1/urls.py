from django.urls import path
from . import views

urlpatterns = [
    path('',views.home1,name='home1'),
    path('register/',views.register,name='register'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('user_login/',views.user_login,name='user_login'),
    path('home2/',views.home2,name='home2'),
    path('styles/<int:category_id>/',views.styles,name='styles'),
    path('teachers/<int:style_id>/',views.teachers,name='teachers'),
    path('videos/<int:teacher_id>/',views.videos,name='videos'),
    path('pay/<int:teacher_id>/',views.create_payment,name='pay'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),

    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    
    path('refund/', views.refund, name='refund'),
    path('shipping/', views.shipping, name='shipping'),

]

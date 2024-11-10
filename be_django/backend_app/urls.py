# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register', views.register, name='register'),
#     path('login', views.login, name='login'),
#     path('user/me', views.user_info, name='user_info'),
#     path('admin_permission', views.AdminPermissionView.as_view(), name='admin_permission'),
#     path('standard_permission', views.StandardPermissionView.as_view(), name='standard_permission'),
#     path('ping/', views.ping, name='ping'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('user/me', views.user_info, name='user_info'),
    path('admin_permission', views.admin_permission, name='admin_permission'),
    path('standard_permission', views.standard_permission, name='standard_permission'),
    path('admin_standard_permission', views.admin_standard_permission, name='admin_standard_permission'),
    path('ping/', views.ping, name='ping'),
]

from django.urls import path
from . import views


urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-weight/', views.add_weight, name='add_weight'),
    path('weight-history/', views.weight_list, name='weight_list'),
    path('edit-weight/<int:id>/', views.edit_weight, name='edit_weight'),
    path('delete-weight/<int:id>/', views.delete_weight, name='delete_weight'),
    path('logout/', views.user_logout, name='logout'),
]
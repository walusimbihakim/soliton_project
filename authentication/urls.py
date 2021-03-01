from django.urls import path
from authentication import views

urlpatterns = [
    # path('accounts/login/', views.login_page, name="loginAccounts"),
    path('login/', views.user_login_view, name="login"),
    path('users/', views.manage_user_view, name='manage_users'),
    path('edit_user/<int:id>/', views.edit_user_view, name='edit_user'),
    path('delete_user/<int:id>/', views.delete_user_view, name='delete_user'),
]

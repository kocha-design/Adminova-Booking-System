from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
        # Password Change URLs
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html', 
        success_url='/accounts/profile/'
    ), name='password_change'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('update-role/<int:user_id>/', views.update_user_role, name='update_user_role'),
    path('manage-users/create/', views.create_user, name='create_user'),
    path('manage-users/toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('register/',views.register,name="register"),
    path('links/',views.links,name='links'),
    path('users/',views.users,name='users'),     
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('delete_link/<int:id>',views.delete_link,name='delete_link'),
    path('settings/',views.settings,name='settings'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="passwords/reset_password.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="passwords/password_reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="passwords/password_reset_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="passwords/password_reset_complete.html"),name="password_reset_complete"),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('activate/<slug:token>', views.verify, name='activate'),
    path("change_user_password/<int:pk>", views.ChangeUserPassword.as_view(), name="change_user_password"),
    path("delete_user/<int:token>", views.delete_user_account, name="delete_user"),
    path("profile_user/<int:pk>", views.profile_user, name="profile_user"),
    path("settings-page/options/", views.settings_page, name="settings_page"),
    path("update-profile/<int:pk>", views.update_user_profile, name="update_user_profile"),

    # User Password Reset URL's
	path("password_reset", auth_view.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
	path("password_reset_done", auth_view.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
	path("reset_password/<uidb64>/<token>", auth_view.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
	path("password_reset/done", auth_view.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]




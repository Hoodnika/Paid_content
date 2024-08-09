from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import path
from django.views.decorators.cache import cache_page

from main_app.services import email_confirm
from user_app.apps import UserAppConfig
from user_app.views import UserLoginView, RegisterView, ProfileView, UserPasswordResetView, user_auto_generate_password, \
    UserPasswordResetConfirmView, payment_success, ProfileUpdateView, SMSVerificationView

app_name = UserAppConfig.name

urlpatterns = [
    path('login/', cache_page(60)(UserLoginView.as_view(template_name='user_app/login.html')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', cache_page(120)(RegisterView.as_view()), name='register'),

    # path('email-confirm/<str:token_verification>/', email_confirm, name='email-confirm'),

    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/auto-generate/done/', user_auto_generate_password, name='password_reset_auto_generate_done'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='clientapp/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='clientapp/password_reset_complete.html'),
         name='password_reset_complete'),

    path('payment_success/', payment_success, name='payment_success'),

    path('profile/<int:pk>/', cache_page(10)(ProfileView.as_view()), name='profile'),
    path('profile/update/<int:pk>/', cache_page(10)(ProfileUpdateView.as_view()), name='profile_update'),
    path('verify-sms/', SMSVerificationView.as_view(), name='sms_verification'),
]

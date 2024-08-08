from django.contrib import admin

from user_app.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'phone_number', 'pk')
    list_filter = ('email', 'is_superuser')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'price', 'session_id', 'is_paid', 'created_at', 'paid_at')

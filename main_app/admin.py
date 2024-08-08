from django.contrib import admin

from main_app.models import Publication, Subscription


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'preview', 'updated_at', 'slug', 'pk')
    list_filter = ('owner', 'title', 'updated_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'is_active', 'update_at', 'end_at', 'pk')
    list_filter = ('owner', 'is_active', 'update_at')

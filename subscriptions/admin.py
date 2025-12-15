from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription

# Register your models here.

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'started_at', 'expires_at')
    list_filter = ('status', 'plan')

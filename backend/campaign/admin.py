from django.contrib import admin
from .models import Participant, Region, Activity


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'region', 'role', 'created_at', 'is_active']
    list_filter = ['role', 'region', 'is_active', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'region']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['governorate', 'participant_count', 'delegation_count', 'created_at']
    search_fields = ['governorate']
    ordering = ['governorate']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'participant_count', 'created_at']
    list_filter = ['activity_type']
    search_fields = ['title', 'description']

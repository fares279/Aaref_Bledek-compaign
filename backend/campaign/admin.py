from django.contrib import admin
from .models import Participant, Region, Activity


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'region', 'role', 'is_active', 'created_at']
    readonly_fields = ['created_at']
    list_per_page = 25


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

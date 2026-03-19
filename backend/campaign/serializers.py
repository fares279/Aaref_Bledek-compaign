from rest_framework import serializers
from .models import Participant, Region, Activity


class ParticipantSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'full_name', 'email', 'phone', 'region', 'role', 'role_display', 'motivation', 'created_at']
        read_only_fields = ['id', 'created_at', 'role_display']

    def validate_email(self, value):
        if Participant.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("A participant with this email already exists.")
        return value.lower()

    def validate_motivation(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Please tell us more about your motivation (at least 20 characters).")
        return value


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

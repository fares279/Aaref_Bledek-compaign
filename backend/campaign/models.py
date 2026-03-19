from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Region(models.Model):
    governorate = models.CharField(max_length=50, unique=True)
    delegation_count = models.IntegerField(default=0)
    participant_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['governorate']

    def __str__(self):
        return self.governorate


class Participant(models.Model):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('contributor', 'Contributor'),
        ('volunteer', 'Research Volunteer'),
        ('ambassador', 'Community Ambassador'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?2?1?6?\d{8}$',
        message='Enter a valid Tunisian phone number.'
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(validators=[phone_regex], max_length=25)
    region = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    motivation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} — {self.get_role_display()}"


class Activity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('exploration', 'Regional Exploration'),
        ('education', 'Educational Resources'),
        ('discussion', 'Community Discussions'),
        ('contribution', 'Knowledge Contributions'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    icon = models.CharField(max_length=50, default='🎯')
    participant_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['activity_type']

    def __str__(self):
        return self.title

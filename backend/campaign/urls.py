from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, RegionViewSet, ActivityViewSet, campaign_stats

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', campaign_stats, name='campaign-stats'),
]

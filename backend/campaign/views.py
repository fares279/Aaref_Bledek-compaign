from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Participant, Region, Activity
from .serializers import ParticipantSerializer, RegionSerializer, ActivitySerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.filter(is_active=True)
    serializer_class = ParticipantSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()
            region_name = participant.region
            region, created = Region.objects.get_or_create(
                governorate=region_name,
                defaults={'delegation_count': 1}
            )
            if not created:
                region.participant_count += 1
                region.save()
            return Response(
                {'success': True, 'message': 'Welcome to the #Aaref_Bledek movement!', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


@api_view(['GET'])
def campaign_stats(request):
    total = Participant.objects.filter(is_active=True).count()
    regions = Region.objects.count()
    roles = Participant.objects.values('role').annotate(count=Count('role'))
    role_dict = {item['role']: item['count'] for item in roles}
    return Response({
        'total_participants': total,
        'total_regions': regions,
        'learners': role_dict.get('learner', 0),
        'contributors': role_dict.get('contributor', 0),
        'volunteers': role_dict.get('volunteer', 0),
        'ambassadors': role_dict.get('ambassador', 0),
    })

from facility_feed_service.utils.paginations import DefaultPagination
from rest_framework import generics
from .models import Facility
from .serializers import FacilitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


class FacilityListCreateView(generics.ListCreateAPIView):
    """List all facilities or create a new one with filtering, searching, and ordering."""
    queryset = Facility.objects.all().order_by("id")
    serializer_class = FacilitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "street_address", "postal_code"]
    filterset_fields = ["country", "locality", "region"]
    ordering_fields = ["name", "country", "locality"]
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]


class FacilityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated]

from django.urls import path

from feed_service.views import FacilityListCreateView, FacilityRetrieveUpdateDestroyView
# Facility Feed Service API endpoints for managing facility data.

urlpatterns = [
    path('', FacilityListCreateView.as_view(), name='facility-list-create'),
    path('<int:pk>/', FacilityRetrieveUpdateDestroyView.as_view(), name='facility-retrieve-update-destroy'),
]

from rest_framework import viewsets

from learning.api.serializers import (
    LocationSerializer
)
from learning.models import (
    Location
)

from utils.permissions import PublicReadOnly


class LocationViewSet(viewsets.ModelViewSet):

	permission_classes = [PublicReadOnly]

	serializer_class = LocationSerializer
	# http_method_names = ['get', 'post', 'put']
	queryset = Location.objects.all()

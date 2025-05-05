from rest_framework import generics, status
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().prefetch_related('images', 'amenities')
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        property = serializer.save()

        response_serializer = PropertySerializer(property)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all().prefetch_related('images', 'amenities')
    serializer_class = PropertySerializer
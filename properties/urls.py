from django.urls import path
from .views import PropertyListCreateView, PropertyDetailView

app_name = 'properties'

urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
]
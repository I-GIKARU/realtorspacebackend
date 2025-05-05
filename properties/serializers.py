from rest_framework import serializers
from .models import Property, PropertyImage, Amenity, Management


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

    def to_representation(self, instance):
        return instance.image.url  # Return just the URL string


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name']


class ManagementSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Management
        fields = ['name', 'type', 'contact', 'photo']

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url  # Return full Cloudinary URL
        return None

class PropertySerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.URLField(),
        source='images.all',
        read_only=True
    )
    amenities = AmenitySerializer(many=True, read_only=True)
    management = ManagementSerializer(read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000,
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True,
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'category', 'description', 'price',
            'bedrooms', 'bathrooms', 'area', 'location',
            'virtual_tour', 'images', 'amenities', 'management',
            'uploaded_images'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        amenities_data = validated_data.pop('amenities', [])
        management_data = validated_data.pop('management', None)

        property = Property.objects.create(**validated_data)

        # Create multiple property images
        for image in uploaded_images:
            PropertyImage.objects.create(property=property, image=image)

        # Create amenities
        for amenity in amenities_data:
            Amenity.objects.create(property=property, **amenity)

        # Create management if data exists
        if management_data:
            Management.objects.create(property=property, **management_data)

        return property
from django.db import models
from cloudinary.models import CloudinaryField


class Property(models.Model):
    CATEGORY_CHOICES = [
        ('Single Room', 'Single Room'),
        ('One Bedroom', 'One Bedroom'),
        ('Two Bedroom', 'Two Bedroom'),
        ('Three Bedroom+', 'Three Bedroom+'),
        ('Apartment', 'Apartment'),
        ('House', 'House'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area = models.PositiveIntegerField(help_text="Area in square feet")
    location = models.CharField(max_length=200)
    virtual_tour = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return self.image.url


class Amenity(models.Model):
    property = models.ForeignKey(Property, related_name='amenities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Management(models.Model):
    TYPE_CHOICES = [
        ('Landlord', 'Landlord'),
        ('Agent', 'Agent'),
        ('Owner', 'Owner'),
    ]

    property = models.OneToOneField(Property, related_name='management', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    contact = models.CharField(max_length=20)
    photo = CloudinaryField('photo')

    def __str__(self):
        return f"{self.type}: {self.name}"
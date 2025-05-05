from django.contrib import admin
from .models import Property, PropertyImage, Amenity, Management


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, AmenityInline]
    list_display = ('name', 'category', 'price', 'location')

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'type', 'contact')

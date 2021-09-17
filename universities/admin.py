from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import University

@admin.register(University)
class UniversityAdmin(OSMGeoAdmin):
    '''University Admin'''
    list_display = ('uni_name', 'location')
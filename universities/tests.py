import json
from django.http import response
from django.test import TestCase, SimpleTestCase
from django.test.client import Client
from django.urls import reverse, resolve
from django.contrib.gis.geos import Point
from . import views
from .models import University


class TestUniversityUrls(SimpleTestCase):

    def test_university_map_view_url_resolves_correct_view(self):
        url = reverse('universities:map')
        self.assertEquals(resolve(url).func.view_class, views.UniversityMapView)


class TestFilterView(TestCase):

    def setUp(self):
        self.test_uni = University.objects.create(
            uni_name='Test',
            location = Point(1,1)
        )
        self.client = Client()

    def test_url_resolves_correct_view(self):
        response = self.client.get(reverse('universities:filter'))
        url = reverse('universities:filter')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(resolve(url).func, views.filter_view)

    def test_view_returns_correct_queryset(self):
        data = {'uni_name': 'Test'}
        response = self.client.get('/ajax/filter', data)
        self.assertEquals(response.status_code, 301)




import json
from django.core import serializers

from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from django.contrib.gis.geos import Polygon
from django.http import JsonResponse

from .models import University, TestUniversity

class UniversityMapView(TemplateView):

    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university'] = json.loads(serialize("geojson", University.objects.all()))
        context['uni'] = University.objects.all()
        return context


def filter_view(request):
    if request.is_ajax and request.method == 'GET':
        # get value from client side
        uni_name = request.GET.get('uni_name', None)
        # return universities by name
        universities = University.objects.filter(uni_name=uni_name)
        data = json.loads(serialize("geojson", universities))
        return JsonResponse({"uganda-universities-domains": data})

def test_uni_list_view(request):
    if request.is_ajax and request.method == 'GET':
        # check the section i.e test
        section = request.GET.get('section', None)
        if section == 'test':
            # return test universities
            universities = json.loads(serialize("geojson", TestUniversity.objects.all()))
            return JsonResponse({"test-universities-data": universities})
    return JsonResponse({}, status = 400)
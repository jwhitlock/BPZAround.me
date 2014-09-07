'''Context processors to add data to bpz templates'''

from django.conf import settings


def mapbox(request):
    return {
        'MAPBOX_TOKEN': getattr(settings, 'MAPBOX_TOKEN'),
        'MAPBOX_ID': getattr(settings, 'MAPBOX_ID'),
    }

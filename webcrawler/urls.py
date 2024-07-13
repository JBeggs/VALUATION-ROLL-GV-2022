# urls.py
from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from .views import ValuationRollViewSet


router = DefaultRouter()
router.register('valuationroll', ValuationRollViewSet)

urlpatterns = [
    re_path('^', include(router.urls)),
]
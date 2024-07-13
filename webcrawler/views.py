# views.py
import django_filters.rest_framework
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.viewsets import GenericViewSet

from .models import ValuationRoll
from .serializers import ValuationRollSerializer
from rest_framework import filters


class ValuationRollViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many Companies
    """
    Valuation Roll Viewset
    
    Defines the rest frame working filtering, quertuset, search and ordering values.
    
    
    """
    serializer_class = ValuationRollSerializer
    queryset = ValuationRoll.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['rate_number', 'roll_type', 'legal_description', 'use_code', 'market_value']
    ordering_fields = ['address', 'market_value']

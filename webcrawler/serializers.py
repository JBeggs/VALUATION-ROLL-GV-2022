# serializers.py
from rest_framework.serializers import ModelSerializer

from .models import ValuationRoll

class ValuationRollSerializer(ModelSerializer):
    class Meta:
        model = ValuationRoll
        fields = (
            'rate_number', 'roll_type', 'legal_description', 'use_code', 'market_value', 'suburb', 'deeds_town', 'scheme'
        )
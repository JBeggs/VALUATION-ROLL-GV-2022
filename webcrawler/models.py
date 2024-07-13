from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class RollQue(models.Model):
    """
    Basic Que for when something goes wrong
    """
    id = models.BigAutoField(primary_key=True)
    deeds_town = models.IntegerField()
    suburb = models.IntegerField()
    scheme = models.IntegerField()


class ValuationRoll(models.Model):
    """
    This model stores the Valuation Rolol data
    """
    id = models.BigAutoField(primary_key=True)
    rate_number = models.IntegerField()
    legal_description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    suburb = models.CharField(max_length=55)
    deeds_town = models.CharField(max_length=55)
    scheme = models.CharField(max_length=55)
    
    first_owner = models.CharField(max_length=125)
    use_code = models.CharField(max_length=55)
    
    rating_category = models.CharField(max_length=55)
    
    market_value = models.CharField(max_length=55)
    registered_extent = ArrayField(models.CharField(max_length=200), blank=True)
    
    roll_type = models.CharField(max_length=55)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Order by -created_at
        """
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.first_owner)

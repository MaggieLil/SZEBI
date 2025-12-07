from django.db import models

from .models_definitions.data_models import *
from .models_definitions.enumeration_models import *

# class DataPoint(models.Model):
#     timestamp = models.DateTimeField()
#     source = models.CharField(max_length=128)
#     value = models.FloatField()
#
#     def __str__(self):
#         return f"{self.source} @ {self.timestamp.isoformat()}"

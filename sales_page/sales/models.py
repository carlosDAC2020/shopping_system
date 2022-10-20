from email.policy import default
from django.db import models

"""
class Products(models.Model):# tabla
    # columna             # tpos de datos 
    name = models.CharField(max_length=40)
    units_available = models.IntegerField(default=0)
    worth_unit = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name """
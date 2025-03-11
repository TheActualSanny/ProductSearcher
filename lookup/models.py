from django.db import models

class Products(models.Model):
    '''
        Table where the actual product lookups are stored.
    '''
    product_name = models.CharField(max_length = 400)
    product_url = models.CharField(max_length = 500)
    product_price = models.IntegerField()
    
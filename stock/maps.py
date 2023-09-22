from . import models
from . import serializers

def ProductData(data):
    item = dict(data)
    item['product_category'] = models.ProductCategory.objects.get(
            id=int(item['product_category'])).category
    
    return item
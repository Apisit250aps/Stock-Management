from rest_framework import serializers

from . import models

class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductData
        fields = '__all__'
        
class ShopDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopData
        fields = '__all__'
        
class InputInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputInvoice
        fields = '__all__'
        
class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputData
        fields = '__all__'
        
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreaData
        fields = '__all__'
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductTypeData
        fields = '__all__'
from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category'
    ]
    
    search_fields = list_display

@admin.register(models.ProductTypeData)
class ProductTypeDataAdmin(admin.ModelAdmin):
    list_display = [
        'type_code',
        'type_name'
    ]
    
    search_fields  = [
        'type_name'
    ]
    
@admin.register(models.ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = [
        'product_code',
        'product_name'
        
    ]
    
    search_fields = [
        'product_name'
    ]
    
@admin.register(models.ShopData)
class ShopDataAdmin(admin.ModelAdmin):
    list_display = [
        'shop_code',
        'shop_name',
        'shop_contact'
    ]
    
    search_fields = list_display
    
@admin.register(models.InputInvoice)
class InputInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_no',
        'shop',
        'input_date'
    ]
    
@admin.register(models.InputData)
class InputDataAdmin(admin.ModelAdmin):
    list_display = [
        'invoice'
    ]
    
@admin.register(models.AreaData)
class AreaDataAdmin(admin.ModelAdmin):
    list_display = [
        'area_name'
    ]
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS = (
        (1, "shop"),
        (2, "customer")
    )

# ระเบียนข้อมูลคงคลัง
class ProductData(models.Model):
    
    product_id = models.AutoField(primary_key=True, unique=True)
    product_code = models.CharField(max_length=16, unique=True, null=True)
    product_name = models.CharField(max_length=256)
    unit_cost = models.FloatField()
    product_desc = models.TextField(default="-")
    
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.product_code} {self.product_name}"
    
class ProductTypeData(models.Model):
    
    type_id = models.AutoField(primary_key=True, unique=True)
    type_code = models.CharField(max_length=256)
    type_name = models.CharField(max_length=128)
    
    def __str__(self):
        
        return f"{self.type_code} {self.type_name}"
    
class ProductDelete(models.Model):
    
    product = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=16)
    del_unit = models.IntegerField()
    
    del_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f"{self.product}"

# ระเบียนข้อมูลกลุ่มผู้ผลิต และลูกค้า
class AreaData(models.Model):
    
    area_id = models.AutoField(primary_key=True, unique=True)
    area_name = models.CharField(max_length=128)
    
    
   
class ShopData(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_status = models.IntegerField(choices=STATUS)
    shop_id = models.AutoField(primary_key=True, unique=True)
    shop_code = models.CharField(max_length=16, unique=True, null=True)
    shop_name = models.CharField(max_length=128)
    shop_product_type = models.CharField(max_length=32)
    shop_contact = models.CharField(max_length=64)
    shop_post_code = models.CharField(max_length=5)
    shop_province = models.CharField(max_length=256)
    shop_district = models.CharField(max_length=256)
    shop_subdistrict = models.CharField(max_length=256)
    shop_detail_address = models.CharField(max_length=256)
    shop_area_code = models.ForeignKey(AreaData, on_delete=models.CASCADE,  null=True)
    shop_tel = models.CharField(max_length=10)
    shop_fax = models.CharField(max_length=10)
    shop_email = models.CharField(max_length=64)
    shop_remark = models.TextField(default="-")
    
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return f"{self.shop_code} {self.shop_name}"


class CustomerData(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_status = models.IntegerField(choices=STATUS)
    customer_id = models.AutoField(primary_key=True, unique=True)
    customer_code = models.CharField(max_length=16)
    customer_name = models.CharField(max_length=256)
    customer_post_code = models.CharField(max_length=5)
    customer_province = models.CharField(max_length=256)
    customer_district = models.CharField(max_length=256)
    customer_subdistrict = models.CharField(max_length=256)
    customer_detail_address = models.CharField(max_length=256)
    customer_tel = models.CharField(max_length=10)
    customer_fax = models.CharField(max_length=10)
    customer_email = models.CharField(max_length=64)
    customer_remark = models.TextField(default="-")
    
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return self.customer_code+" "+self.customer_name
 

# ระเบียนรายการรับสินค้าเข้า และจ่ายสินค้าออก 
# เอกสารการรับสินค้า
class InputInvoice(models.Model):
    
    invoice_id = models.AutoField(primary_key=True, unique=True)
    invoice_no = models.CharField(max_length=16, unique=True, null=True)
    shop = models.ForeignKey(ShopData, on_delete=models.CASCADE)
    total_price = models.FloatField()
    discount = models.FloatField()
    remark = models.TextField(default="-")
    
    input_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        
        return self.invoice_no
    
# การรับสินค้า
class InputData(models.Model):
    
    invoice = models.ForeignKey(InputInvoice, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=16,  null=True)
    product = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField()
    
    def __str__(self):
    
        return self.invoice_no
    
# เอกสารการจ่าสินค้าออก
class OutputInvoice(models.Model):
    
    invoice_id = models.AutoField(primary_key=True, unique=True)
    invoice_no = models.CharField(max_length=16, unique=True, null=True)
    customer = models.ForeignKey(CustomerData, on_delete=models.CASCADE)
    total_price = models.FloatField()
    discount = models.FloatField()
    remark = models.TextField(default="-")
    
    input_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
    
        return self.invoice_no

# การจ่าสินค้าออก
class OutputData(models.Model):
    
    invoice = models.ForeignKey(OutputInvoice, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=16,  null=True)
    product = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sale_price = models.FloatField()
    discount = models.FloatField()
    
    def __str__(self):
        
        return self.invoice_no
      
    
class DBCounter(models.Model):
    
    counter_type = models.CharField(max_length=16, primary_key=True, unique=True)
    counter_number = models.IntegerField()
 
class DBDateCounter(models.Model):
    
    counter_type = models.ForeignKey(DBCounter, on_delete=models.CASCADE)
    counter_number = models.IntegerField()
    counter_date = models.DateTimeField(auto_now_add=True)
    
    
class TempInputDB(models.Model):
    
    invoice = models.CharField(max_length=16)
    invoice_no = models.CharField(max_length=16)
    product = models.CharField(max_length=16)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    discount = models.FloatField()
    
    def __str__(self):
        
        return self.invoice_no
    
class TempOutputDB(models.Model):
    
    invoice = models.CharField(max_length=16)
    invoice_no = models.CharField(max_length=16)
    product = models.CharField(max_length=16)
    quantity = models.IntegerField()
    sale_price = models.FloatField()
    discount = models.FloatField()

    def __str__(self):
            
            return self.invoice_no
# Generated by Django 4.2.3 on 2023-08-19 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_shopdata_shop_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdata',
            name='product_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.productcategory'),
        ),
    ]

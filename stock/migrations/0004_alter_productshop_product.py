# Generated by Django 4.2.3 on 2023-09-22 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_productshop_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productshop',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='stock.productdata'),
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttypedata',
            name='type_code',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
# Generated by Django 4.2.6 on 2023-11-04 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_customer_zipcode_remove_product_composition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='selling_price',
            field=models.FloatField(),
        ),
    ]

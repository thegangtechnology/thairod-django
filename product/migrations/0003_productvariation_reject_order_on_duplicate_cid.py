# Generated by Django 3.2.5 on 2021-08-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_productvariation_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='reject_order_on_duplicate_cid',
            field=models.BooleanField(default=False),
        ),
    ]
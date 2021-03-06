# Generated by Django 3.2.5 on 2021-07-30 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0009_alter_shipment_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='deliver',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Order for shipment created'), ('BOOKED', 'Book shipment to Shippop'), ('CONFIRMED', 'Confirmed shipment')], default='CREATED', max_length=9),
        ),
    ]

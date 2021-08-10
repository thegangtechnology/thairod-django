# Generated by Django 3.2.6 on 2021-08-09 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0020_alter_shipment_shippop_confirm_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='booked_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='shipment',
            name='fulfilled_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Order for shipment created'), ('FULFILLED', 'All Order Items are Fulfilled'), ('BOOKED', 'Book shipment to Shippop'), ('CONFIRMED', 'Confirmed shipment')], default='CREATED', max_length=9),
        ),
    ]

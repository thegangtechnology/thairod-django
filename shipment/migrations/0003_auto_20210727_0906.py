# Generated by Django 3.2.5 on 2021-07-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0002_rename_purchase_id_shipment_shippop_purchase_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trackingstatus',
            name='courier_code',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='courier_tracking_code',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='discount',
            field=models.DecimalField(decimal_places=0.3, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trackingstatus',
            name='price',
            field=models.DecimalField(decimal_places=0.3, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trackingstatus',
            name='status',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trackingstatus',
            name='tracking_code',
            field=models.CharField(max_length=20),
        ),
    ]

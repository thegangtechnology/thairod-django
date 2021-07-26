# Generated by Django 3.2.5 on 2021-07-26 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='shipment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shipment.shipment'),
            preserve_default=False,
        ),
    ]

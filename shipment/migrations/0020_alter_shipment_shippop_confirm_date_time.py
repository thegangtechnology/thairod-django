# Generated by Django 3.2.6 on 2021-08-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0019_confirmation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='shippop_confirm_date_time',
            field=models.DateTimeField(db_index=True, default=None, null=True),
        ),
    ]
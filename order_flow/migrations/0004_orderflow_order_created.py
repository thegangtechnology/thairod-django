# Generated by Django 3.2.6 on 2021-08-10 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_flow', '0003_orderflow_auto_doctor_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderflow',
            name='order_created',
            field=models.BooleanField(default=False),
        ),
    ]
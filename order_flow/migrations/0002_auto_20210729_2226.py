# Generated by Django 3.2.5 on 2021-07-29 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_flow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderflow',
            name='doctor_order',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderflow',
            name='patient_confirmation',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderflow',
            name='patient_link_hash',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

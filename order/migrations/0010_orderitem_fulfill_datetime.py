# Generated by Django 3.2.5 on 2021-08-04 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20210805_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='fulfill_datetime',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

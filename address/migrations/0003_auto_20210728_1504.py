# Generated by Django 3.2.5 on 2021-07-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_alter_address_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='telno',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='lon',
            field=models.DecimalField(decimal_places=7, max_digits=15, null=True),
        ),
    ]

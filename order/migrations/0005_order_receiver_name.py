# Generated by Django 3.2.5 on 2021-07-30 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20210728_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receiver_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
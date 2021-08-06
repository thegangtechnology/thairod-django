# Generated by Django 3.2.5 on 2021-08-05 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('default_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
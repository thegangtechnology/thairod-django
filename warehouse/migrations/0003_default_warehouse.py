# Generated by Django 3.2.5 on 2021-08-05 13:55

from django.db import migrations


def forward(apps, schema_editor):
    warehouse_model = apps.get_model('warehouse', 'Warehouse')
    default_warehouse_model = apps.get_model('warehouse', 'DefaultWarehouse')
    address_model = apps.get_model('address', 'Address')

    address = address_model.objects.create(
        name="โกดังหลักไทยรอด",
        lat=None,
        lon=None,
        house_number = 'เลขที่ 599 สามแยกกล้วยน้ำไท',
        subdistrict = 'คลองเตย',
        district='คลองเตย',
        province='กรุงเทพมหานคร',
        postal_code = '10100',
        country='ไทย',
        telno='0928908989',
        note=''
    )

    warehouse_model.objects.create(
        name='โกดังหลักไทยรอด',
        tel='',
        address_id=address.id
    )

    default_warehouse_model.objects.create(
        id=1,
        default_warehouse_id=warehouse_model.objects.first().id
    )


def backward(apps, schema_editor):
    default_warehouse_model = apps.get_model('warehouse', 'Warehouse')
    default_warehouse_model.get(id=1).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('warehouse', '0002_defaultwarehouse'),
    ]

    operations = [

        migrations.RunPython(forward, reverse_code=backward),

    ]
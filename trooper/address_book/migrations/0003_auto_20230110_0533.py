# Generated by Django 3.2.16 on 2023-01-10 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0002_auto_20221214_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='object_id',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='email',
            name='object_id',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='phone',
            name='object_id',
            field=models.UUIDField(),
        ),
    ]
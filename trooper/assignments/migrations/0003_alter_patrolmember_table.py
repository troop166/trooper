# Generated by Django 3.2.17 on 2023-02-16 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_alter_committeemember_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='patrolmember',
            table='assignments_patrol_member',
        ),
    ]
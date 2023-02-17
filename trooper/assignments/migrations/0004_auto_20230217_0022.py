# Generated by Django 3.2.17 on 2023-02-17 00:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0003_alter_patrolmember_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Leadership',
            new_name='Leader',
        ),
        migrations.AlterModelOptions(
            name='leader',
            options={'ordering': ['-start', '-role', 'member'], 'verbose_name': 'Leader', 'verbose_name_plural': 'Leaders'},
        ),
    ]

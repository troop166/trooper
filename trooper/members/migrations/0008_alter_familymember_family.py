# Generated by Django 3.2.16 on 2023-01-25 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_member_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', related_query_name='family_member', to='members.family'),
        ),
    ]
# Generated by Django 3.2.16 on 2022-10-23 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('P', 'Parent'), ('C', 'CHILD')], max_length=1, verbose_name='role')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.family')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Family Member',
                'verbose_name_plural': 'Family Members',
            },
        ),
        migrations.AddField(
            model_name='family',
            name='members',
            field=models.ManyToManyField(related_name='families', through='members.FamilyMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
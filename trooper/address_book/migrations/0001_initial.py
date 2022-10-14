# Generated by Django 3.2.16 on 2022-10-14 22:11

from django.db import migrations, models
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, choices=[('H', 'Home'), ('W', 'Work'), ('B', 'P.O. Box'), ('O', 'Other')], max_length=1, verbose_name='label')),
                ('street', models.CharField(max_length=150, verbose_name='street')),
                ('street2', models.CharField(blank=True, help_text='e.g. Apartment, Suite, Box Number', max_length=150, verbose_name='street 2')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(max_length=2, verbose_name='state')),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10, verbose_name='ZIP code')),
                ('is_published', models.BooleanField(default=True, help_text='Allow other members to see this address in the Troop directory.', verbose_name='publish in the directory')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, choices=[('H', 'Home'), ('W', 'Work'), ('O', 'Other')], max_length=1, verbose_name='label')),
                ('address', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_published', models.BooleanField(default=True, help_text='Allow other members to see this address in the Troop directory.', verbose_name='publish in directory')),
                ('is_subscribed', models.BooleanField(default=True, help_text='Receive Troop communications at this email address. ', verbose_name='subscribed to mailing lists')),
            ],
            options={
                'verbose_name': 'Email Address',
                'verbose_name_plural': 'Email Addresses',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, choices=[('H', 'Home'), ('M', 'Mobile'), ('W', 'Work'), ('O', 'Other')], max_length=1, verbose_name='label')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number')),
                ('is_published', models.BooleanField(default=True, help_text='Allow other members to see this number in the Troop directory.', verbose_name='publish in directory')),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
            },
        ),
    ]

# Generated by Django 3.2.18 on 2023-04-06 23:56

from django.db import migrations, models
import django.db.models.deletion
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
                ('street', models.CharField(max_length=150, verbose_name='street')),
                ('street2', models.CharField(blank=True, help_text='e.g. Apartment, Suite, Box Number', max_length=150, verbose_name='street 2')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(max_length=2, verbose_name='state')),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10, verbose_name='ZIP code')),
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
                ('address', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
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
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number')),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address_book.address')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ('name',),
            },
        ),
    ]

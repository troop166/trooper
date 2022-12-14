# Generated by Django 3.2.16 on 2022-12-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Allow others to see this address in the member directory.', verbose_name='published in directory'),
        ),
        migrations.AlterField(
            model_name='email',
            name='is_subscribed',
            field=models.BooleanField(default=True, help_text='Receive periodic email communications at this address.', verbose_name='subscribed to mailing lists'),
        ),
    ]

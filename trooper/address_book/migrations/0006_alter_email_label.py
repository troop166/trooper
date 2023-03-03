# Generated by Django 3.2.18 on 2023-03-03 00:55

from django.db import migrations, models


def forwards(apps, schema_editor):
    Email = apps.get_model("address_book", "Email")
    for email in Email.objects.all():
        if email.label == "H":
            email.label = "HOME"
        if email.label == "W":
            email.label = "WORK"
        if email.label == "S":
            email.label = "SCHOOL"
        if email.label == "O":
            email.label = ""
        email.save()


def reverse(apps, schema_editor):
    Email = apps.get_model("address_book", "Email")
    for email in Email.objects.all():
        if email.label == "HOME":
            email.label = "H"
        if email.label == "SCHOOL":
            email.label = "S"
        if email.label == "WORK":
            email.label = "W"
        email.save()


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0005_alter_phone_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='label',
            field=models.CharField(blank=True, choices=[('HOME', 'Home'), ('SCHOOL', 'School'), ('WORK', 'Work')], max_length=6, verbose_name='label'),
        ),
        migrations.RunPython(forwards, reverse),
    ]

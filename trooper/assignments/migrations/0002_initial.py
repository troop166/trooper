# Generated by Django 3.2.18 on 2023-04-06 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import trooper.members.models.people


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assignments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='patrolmember',
            name='member',
            field=models.ForeignKey(limit_choices_to=trooper.members.models.people.Member.youth_choices, on_delete=django.db.models.deletion.CASCADE, related_name='patrol_members', related_query_name='patrol_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patrolmember',
            name='patrol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patrol_members', related_query_name='patrol_member', to='assignments.patrol'),
        ),
        migrations.AddField(
            model_name='patrol',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='patrols', through='assignments.PatrolMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leader',
            name='member',
            field=models.ForeignKey(limit_choices_to=trooper.members.models.people.Member.adult_choices, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='committee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committee_members', related_query_name='committee_member', to='assignments.committee'),
        ),
        migrations.AddField(
            model_name='committeemember',
            name='member',
            field=models.ForeignKey(limit_choices_to=trooper.members.models.people.Member.adult_choices, on_delete=django.db.models.deletion.CASCADE, related_name='committee_members', related_query_name='committee_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='committee',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='committees', through='assignments.CommitteeMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
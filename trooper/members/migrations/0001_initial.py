# Generated by Django 4.2 on 2023-04-12 18:46

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import trooper.members.managers
import trooper.members.utils
import trooper.members.validators
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("address_book", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A member with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=100, verbose_name="first name"),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="middle name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="last name"),
                ),
                (
                    "suffix",
                    models.CharField(blank=True, max_length=10, verbose_name="suffix"),
                ),
                (
                    "nickname",
                    models.CharField(
                        blank=True,
                        help_text="The name this member prefers to be known by.",
                        max_length=100,
                        verbose_name="nickname",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="A profile photo is used in the site directory to assist members match names with faces. A good photo is one taken from the shoulders up with the face clearly visible. Photos are only available to active members and never shared outside of the Troop.",
                        null=True,
                        upload_to=trooper.members.utils.get_member_photo_upload_to,
                        verbose_name="profile picture",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        max_length=1,
                        verbose_name="gender",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        validators=[trooper.members.validators.date_of_birth_validator],
                        verbose_name="date of birth",
                    ),
                ),
                (
                    "date_of_death",
                    models.DateField(
                        blank=True,
                        null=True,
                        validators=[trooper.members.validators.date_of_death_validator],
                        verbose_name="date of death",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Member",
                "verbose_name_plural": "Members",
                "ordering": ["last_name", "nickname", "first_name"],
            },
            managers=[
                ("objects", trooper.members.managers.MemberManager()),
            ],
        ),
        migrations.CreateModel(
            name="Family",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Family",
                "verbose_name_plural": "Families",
            },
        ),
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                (
                    "phonenumber_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="address_book.phonenumber",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HOME", "Home"),
                            ("CELL", "Mobile"),
                            ("FAX", "Fax"),
                            ("WORK", "Work"),
                        ],
                        max_length=4,
                        verbose_name="label",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Allow other members to see this number in the member directory.",
                        verbose_name="published in directory",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phone_numbers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("address_book.phonenumber",),
        ),
        migrations.CreateModel(
            name="FamilyMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("P", "Parent"), ("C", "Child")],
                        max_length=1,
                        verbose_name="role",
                    ),
                ),
                (
                    "family",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="family_members",
                        related_query_name="family_member",
                        to="members.family",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="family_members",
                        related_query_name="family_member",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Family Member",
                "verbose_name_plural": "Family Members",
                "db_table": "members_family_member",
            },
        ),
        migrations.AddField(
            model_name="family",
            name="members",
            field=models.ManyToManyField(
                related_name="families",
                through="members.FamilyMember",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="EmailAddress",
            fields=[
                (
                    "emailaddress_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="address_book.emailaddress",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HOME", "Home"),
                            ("SCHOOL", "School"),
                            ("WORK", "Work"),
                        ],
                        max_length=6,
                        verbose_name="label",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Allow others to see this address in the member directory.",
                        verbose_name="published in directory",
                    ),
                ),
                (
                    "is_subscribed",
                    models.BooleanField(
                        default=True,
                        help_text="Receive periodic email communications at this address.",
                        verbose_name="subscribed to mailing lists",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_addresses",
                        related_query_name="email_address",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("address_book.emailaddress",),
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "address_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="address_book.address",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("HOME", "Home"),
                            ("WORK", "Work"),
                            ("SCHOOL", "School"),
                            ("POB", "P.O. Box"),
                        ],
                        max_length=6,
                        verbose_name="label",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Allow others to see this address in the member directory.",
                        verbose_name="published in directory",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("address_book.address",),
        ),
    ]

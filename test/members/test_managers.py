import random

from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

User = get_user_model()


def _random_adult_dob():
    now = timezone.now()
    random.seed(now)
    age = random.randint(20, 100)
    return now.replace(year=now.year - age)


class MemberManagersTest(TestCase):
    def test_create_member(self):
        user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="foo",
            gender="M",
            date_of_birth=_random_adult_dob(),
        )

        self.assertEqual(user.username, "user")
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(username="")
        with self.assertRaises(ValueError):
            User.objects.create_user(username="", password="foo")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="forgot_birthday")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="bar",
            gender="M",
            date_of_birth=_random_adult_dob(),
        )

        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_superuser()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username="", password="foo")
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="foo",
                is_superuser=False,
                gender="M",
                date_of_birth=_random_adult_dob(),
            )

    def test_create_member_with_case_insensitive_duplicate_username(self):
        User.objects.create_user(
            username="user",
            password="foo",
            gender="M",
            date_of_birth=_random_adult_dob(),
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="User",
                password="bar",
                gender="M",
                date_of_birth=_random_adult_dob(),
            )

    def test_user_can_authenticate_case_insensitive(self):
        User.objects.create_user(
            username="User",
            password="foo",
            gender="M",
            date_of_birth=_random_adult_dob(),
        )

        lower_case = authenticate(username="user", password="foo")
        upper_case = authenticate(username="USER", password="foo")
        mixed_case = authenticate(username="User", password="foo")
        bad_password = authenticate(username="user", password="Foo")

        self.assertIsNotNone(lower_case)
        self.assertIsNotNone(upper_case)
        self.assertIsNotNone(mixed_case)
        self.assertIsNone(bad_password)

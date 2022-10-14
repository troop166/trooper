from django.test import TestCase

from trooper.address_book.models import Address
from trooper.members.models import Member


class AddressCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create()

    def test_simple_address(self):
        address = Address.objects.create(
            street="123 Main St.",
            city="Seattle",
            state="WA",
            zipcode="98101",
            content_object=self.member,
        )

        self.assertEqual(address.street, "123 Main St.")
        self.assertEqual(address.street2, "")
        self.assertEqual(address.city, "Seattle")
        self.assertEqual(address.state, "WA")
        self.assertEqual(address.zipcode, "98101")
        self.assertEqual(str(address), "123 Main St., Seattle, WA, 98101")
        self.assertTrue(address.is_published)

    def test_multiline_address(self):
        address = Address.objects.create(
            street="321 Any Avenue",
            street2="Suite 1000",
            city="Seattle",
            state="WA",
            zipcode="98101-1010",
            is_published=False,
            label="W",
            content_object=self.member,
        )

        self.assertEqual(address.street, "321 Any Avenue")
        self.assertEqual(address.street2, "Suite 1000")
        self.assertEqual(address.city, "Seattle")
        self.assertEqual(address.state, "WA")
        self.assertEqual(address.zipcode, "98101-1010")
        self.assertEqual(
            str(address), "321 Any Avenue, Suite 1000, Seattle, WA, 98101-1010"
        )
        self.assertFalse(address.is_published)

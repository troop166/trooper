from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_get(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.resolver_match.route, "about/")
        self.assertTemplateUsed(self.response, "website/about.html")


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_get(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.resolver_match.route, "")
        self.assertTemplateUsed(self.response, "website/home.html")

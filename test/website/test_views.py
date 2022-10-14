from http import HTTPStatus

from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class FaviconTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Cache-Control"], "max-age=86400, immutable, public")
        self.assertEqual(response["Content-Type"], "image/x-icon")
        self.assertGreater(len(response.getvalue()), 0)


class AboutPageTests(TestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_get(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.resolver_match.route, "about/")
        self.assertTemplateUsed("about.html")


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_get(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.resolver_match.route, "")
        self.assertTemplateUsed("home.html")

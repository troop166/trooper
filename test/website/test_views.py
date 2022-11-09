import logging
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class AboutPageTests(TestCase):
    def setUp(self):
        url = reverse("about_page")
        self.response = self.client.get(url)

    def test_get(self):
        self.assertEqual(self.response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.response.resolver_match.route, "about/")


class HomePageTests(TestCase):
    def setUp(self):
        url = reverse("home_page")
        self.response = self.client.get(url)

    def test_get(self):
        # TODO: Doesn't work, how do we verify correct logging?
        self.assertLogs("loggers", level=logging.WARNING)
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertEqual(self.response.resolver_match.route, "")
        self.assertTemplateUsed(self.response, "website/home.html")

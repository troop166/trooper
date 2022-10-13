import json
from http import HTTPStatus

from django.test import SimpleTestCase
from django.urls import reverse


class InstallationTest(SimpleTestCase):
    def test_ping_url(self):
        response = self.client.get(reverse("ping"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(content["ping"], "pong")

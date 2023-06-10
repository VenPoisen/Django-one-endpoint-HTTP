from django.test import RequestFactory, TestCase
from django.urls import reverse
from .views import get_response_time
import json


class AppBaseurlViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_response_time_without_dominio_returns_400(self):
        request = self.factory.get(reverse("get_response_time"))
        response = get_response_time(request)

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data['error'],
            "El parámetro 'dominio' es obligatorio"
        )

    def test_get_response_time_with_valid_http_dominio_returns_200(self):
        request = self.factory.get(
            reverse("get_response_time"),
            {'dominio': 'www.example.com'}
        )
        # "www.example.com" has a valid http:// website and does not redirect,
        # thus returning status 200.
        response = get_response_time(request)

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn('status', data)
        self.assertIn('time', data)

    def test_get_response_time_with_valid_https_dominio_redirects_301(self):
        request = self.factory.get(
            reverse("get_response_time"),
            {'dominio': 'www.stackoverflow.com'}
        )
        # "www.stackoverflow.com" does not have a valid http:// website,
        # thus redirecting to https:// ands returning status 301.
        response = get_response_time(request)

        self.assertEqual(response.status_code, 301)

    def test_get_response_time_correct_ip_for_dominio_returns_301(self):
        request = self.factory.get(
            reverse("get_response_time"),
            {
                'dominio': 'www.stackoverflow.com',
                'ip': "151.101.193.69",
            }
        )
        response = get_response_time(request)

        self.assertEqual(response.status_code, 301)

    def test_get_response_time_wrong_ip_for_dominio_returns_500(self):
        request = self.factory.get(
            reverse("get_response_time"),
            {
                'dominio': 'www.microsoft.com',
                'ip': "151.101.193.69",
            }
        )
        response = get_response_time(request)

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            data['error'],
            "500 Server Error: Domain Not Found for url: http://151.101.193.69/"
        )

    def test_get_response_time_with_invalid_ip_returns_500(self):
        request = self.factory.get(
            reverse("get_response_time"),
            {
                'dominio': 'www.stackoverflow.com',
                'ip': '111.111.11.11',
            }
        )
        response = get_response_time(request)

        data = json.loads(response.content)

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

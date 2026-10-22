import unittest
from unittest.mock import Mock, patch

import requests

from clients.http import get_json, NotFoundError, ServiceUnavailableError


class TestHTTP(unittest.TestCase):

    def make_response(self, status=200, data=None, headers=None):
        response = Mock()
        response.status_code = status
        response.headers = headers or {}
        response.json.return_value = {"ok": True} if data is None else data
        response.raise_for_status.return_value = None
        return response

    @patch("clients.http.requests.get")
    def test_success(self, mock_get):
        mock_get.return_value = self.make_response()

        result = get_json("https://example.com")

        self.assertEqual(result, {"ok": True})
        mock_get.assert_called_once_with(
            "https://example.com", params=None, timeout=10
        )

    @patch("clients.http.time.sleep")
    @patch("clients.http.requests.get")
    def test_timeout_retry(self, mock_get, mock_sleep):
        mock_get.side_effect = [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            self.make_response(),
        ]

        self.assertEqual(get_json("https://example.com"), {"ok": True})
        self.assertEqual(mock_get.call_count, 3)

    @patch("clients.http.time.sleep")
    @patch("clients.http.requests.get")
    def test_connection_error_retry(self, mock_get, mock_sleep):
        mock_get.side_effect = [
            requests.exceptions.ConnectionError(),
            requests.exceptions.ConnectionError(),
            self.make_response(),
        ]

        self.assertEqual(get_json("https://example.com"), {"ok": True})
        self.assertEqual(mock_get.call_count, 3)

    @patch("clients.http.time.sleep")
    @patch("clients.http.requests.get")
    def test_server_errors_retry(self, mock_get, mock_sleep):
        for status in (500, 502, 503, 504):
            with self.subTest(status=status):
                mock_get.reset_mock()
                mock_get.side_effect = [
                    self.make_response(status),
                    self.make_response(status),
                    self.make_response(),
                ]

                self.assertEqual(get_json("https://example.com"), {"ok": True})
                self.assertEqual(mock_get.call_count, 3)

    @patch("clients.http.time.sleep")
    @patch("clients.http.requests.get")
    def test_429_retry_after(self, mock_get, mock_sleep):
        mock_get.side_effect = [
            self.make_response(429, headers={"Retry-After": "2"}),
            self.make_response(),
        ]

        self.assertEqual(get_json("https://example.com"), {"ok": True})
        mock_sleep.assert_called_once_with(2.0)

    @patch("clients.http.time.sleep")
    @patch("clients.http.requests.get")
    def test_service_unavailable_after_retries(self, mock_get, mock_sleep):
        mock_get.return_value = self.make_response(503)

        with self.assertRaises(ServiceUnavailableError):
            get_json("https://example.com")

        self.assertEqual(mock_get.call_count, 3)

    @patch("clients.http.requests.get")
    def test_not_found(self, mock_get):
        mock_get.return_value = self.make_response(404)

        with self.assertRaises(NotFoundError):
            get_json("https://example.com")

    @patch("clients.http.requests.get")
    def test_invalid_json(self, mock_get):
        response = self.make_response()
        response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = response

        with self.assertRaises(ServiceUnavailableError):
            get_json("https://example.com")

    @patch("clients.http.requests.get")
    def test_invalid_json_structure(self, mock_get):
        mock_get.return_value = self.make_response(data=[1, 2, 3])

        with self.assertRaises(ServiceUnavailableError):
            get_json("https://example.com")


if __name__ == "__main__":
    unittest.main()
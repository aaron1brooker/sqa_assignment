import unittest
import json
from unittest.mock import patch
from pydantic import ValidationError

from src.flask.router import app
from src.flask.types import OutcomeResponse, FetchItemsResponse


class TestValidateRequestPayload(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch("src.flask.router.logger.error")
    def test_unknown_request_type(self, mock_logger_error):
        with self.client:
            response = self.client.post("/unknown_endpoint", data="{}", content_type="application/json")
            mock_logger_error.assert_called_once_with("Invalid request endpoint")
            self.assertEqual(response.get_json(), OutcomeResponse(success=False).model_dump_json())

    def test_invalid_check_item_request(self):
        with self.client:
            response = self.client.post(
                "/check-item", data=json.dumps({"item_id": 999}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=False).model_dump_json())

    @patch("src.flask.router.check_item_in_db")
    def test_valid_check_item_request(self, mock_check_item):
        mock_check_item.return_item = True
        with self.client:
            response = self.client.post(
                "/check-item", data=json.dumps({"item_id": "item_id_1"}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=True).model_dump_json())

    def test_invalid_delete_item_request(self):
        with self.client:
            response = self.client.post(
                "/delete-item", data=json.dumps({"item_id": 123}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=False).model_dump_json())

    @patch("src.flask.router.delete_item_from_db")
    def test_valid_delete_item_request(self, mock_delete_item):
        mock_delete_item.return_item = True
        with self.client:
            response = self.client.post(
                "/delete-item", data=json.dumps({"item_id": "item123"}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=True).model_dump_json())

    def test_invalid_add_item_request(self):
        with self.client:
            response = self.client.post(
                "/add-item",
                data=json.dumps({"item_id": "item123", "message": 123, "checked": "True"}),
                content_type="application/json",
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=False).model_dump_json())

    @patch("src.flask.router.add_item_to_db")
    def test_valid_add_item_request(self, mock_add_item):
        mock_add_item.return_item = True
        with self.client:
            response = self.client.post(
                "/add-item",
                data=json.dumps({"item_id": "item123", "message": "Added item", "checked": True}),
                content_type="application/json",
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=True).model_dump_json())

    def test_invalid_fetch_items_request(self):
        with self.client:
            response = self.client.post(
                "/fetch-items", data=json.dumps({"user_identifier": "user123"}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), OutcomeResponse(success=False).model_dump_json())

    @patch("src.flask.router.get_all_items")
    def test_valid_fetch_items_request(self, mock_get_all_items):
        mock_get_all_items.return_item = []
        # Simulate valid JSON payload for '/fetch-items' endpoint
        with self.client:
            response = self.client.post(
                "/fetch-items", data=json.dumps({"user_identifier": 123}), content_type="application/json"
            )
            self.assertEqual(response.get_json(), FetchItemsResponse(items=[]).model_dump_json())

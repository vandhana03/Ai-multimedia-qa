from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from unittest.mock import patch


class UploadAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("uploads.views.create_vector_store")
    @patch("uploads.views.extract_pdf_text")
    def test_upload_pdf_success(self, mock_extract_pdf_text, mock_create_vector_store):
        mock_extract_pdf_text.return_value = "sample extracted text"
        file_obj = SimpleUploadedFile(
            "sample.pdf", b"%PDF-1.4 fake", content_type="application/pdf"
        )

        response = self.client.post(
            "/api/upload/",
            {"title": "Test PDF", "file": file_obj},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["file_type"], "pdf")
        self.assertIn("file_url", response.data)
        mock_create_vector_store.assert_called_once()

    def test_upload_missing_file_returns_400(self):
        response = self.client.post(
            "/api/upload/",
            {"title": "No file"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "file is required")

    def test_upload_unsupported_file_type_returns_400(self):
        file_obj = SimpleUploadedFile(
            "sample.txt", b"hello", content_type="text/plain"
        )
        response = self.client.post(
            "/api/upload/",
            {"title": "Bad type", "file": file_obj},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("unsupported file type", response.data["error"])

from django.test import TestCase
from rest_framework.test import APIClient
from uploads.models import UploadedFile
from unittest.mock import patch


class ChatbotAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        UploadedFile.objects.create(
            title="Demo",
            file="uploads/demo.mp4",
            file_type="video",
            extracted_text="At 00:30 we discuss pricing. At 01:20 we discuss onboarding.",
        )

    @patch("chatbot.views.run_multi_agent")
    def test_chat_returns_answer(self, mock_run_multi_agent):
        mock_run_multi_agent.return_value = {"intent": "qa", "answer": "demo answer"}
        response = self.client.post("/api/chat/", {"question": "what is pricing?"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["answer"], "demo answer")
        self.assertEqual(response.data["agent"], "qa")

    @patch("chatbot.views.summarize")
    def test_summary_returns_generated_summary(self, mock_summarize):
        mock_summarize.return_value = "short summary"
        response = self.client.post("/api/summary/", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["summary"], "short summary")

    @patch("chatbot.views.extract_timestamps_structured")
    def test_timestamps_returns_structured_data(self, mock_extract):
        mock_extract.return_value = [
            {"topic": "pricing", "time": "00:30", "seconds": 30}
        ]
        response = self.client.post(
            "/api/timestamps/",
            {"topic": "pricing"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["timestamps"]), 1)
        self.assertEqual(response.data["timestamps"][0]["seconds"], 30)

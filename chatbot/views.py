from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from .graph import run_multi_agent
from .agents.summarizer import summarize
from .agents.timestamp_agent import extract_timestamps_structured
from uploads.models import UploadedFile


def get_latest_upload_with_text():
    return UploadedFile.objects.exclude(
        extracted_text__isnull=True
    ).exclude(
        extracted_text__exact=""
    ).order_by("-created_at").first()


def get_context_for_question(question):
    embeddings = OpenAIEmbeddings()

    latest_upload = get_latest_upload_with_text()
    latest_context = ""
    if latest_upload and latest_upload.extracted_text:
        latest_context = latest_upload.extracted_text[:12000]

    try:
        db = FAISS.load_local(
            "faiss_db",
            embeddings,
            allow_dangerous_deserialization=True
        )
        docs = db.similarity_search(question, k=4)
    except Exception:
        docs = []

    context_parts = []
    for doc in docs:
        text = (doc.page_content or "").strip()
        if text:
            context_parts.append(text)
    context = "\n\n".join(context_parts)

    if latest_context:
        context = latest_context

    return context, latest_upload


class ChatView(APIView):

    def post(self,request):
        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "question is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context, latest_upload = get_context_for_question(question)

        if not context:
            return Response(
                {
                    "error": "No searchable content found. Please upload a file first."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = run_multi_agent(
            {
                "question": question,
                "context": context,
                "transcript": context,
                "topic": question,
            }
        )

        return Response({
            "agent": result.get("intent"),
            "answer": result.get("answer", ""),
            "source_title": latest_upload.title if latest_upload else None,
            "source_file_type": latest_upload.file_type if latest_upload else None,
        })


class SummaryView(APIView):
    def post(self, request):
        latest_upload = get_latest_upload_with_text()
        if not latest_upload:
            return Response(
                {"error": "No uploaded content found. Please upload a file first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = summarize(latest_upload.extracted_text[:12000])
        return Response(
            {
                "summary": summary,
                "source_title": latest_upload.title,
                "source_file_type": latest_upload.file_type,
            }
        )


class TimestampView(APIView):
    def post(self, request):
        topic = request.data.get("topic", "").strip()
        if not topic:
            return Response(
                {"error": "topic is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        latest_upload = get_latest_upload_with_text()
        if not latest_upload:
            return Response(
                {"error": "No uploaded content found. Please upload a file first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transcript = latest_upload.extracted_text[:16000]
        timestamps = extract_timestamps_structured(transcript, topic)

        return Response(
            {
                "topic": topic,
                "timestamps": timestamps,
                "source_title": latest_upload.title,
                "source_file_type": latest_upload.file_type,
            }
        )
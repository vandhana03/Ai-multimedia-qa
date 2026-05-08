from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from .graph import run_multi_agent
from uploads.models import UploadedFile

class ChatView(APIView):

    def post(self,request):
        question = request.data.get("question", "").strip()

        if not question:
            return Response(
                {"error": "question is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        embeddings = OpenAIEmbeddings()

        latest_upload = UploadedFile.objects.exclude(
            extracted_text__isnull=True
        ).exclude(
            extracted_text__exact=""
        ).order_by("-created_at").first()

        # Prefer the latest uploaded content so chat answers map to the user's
        # most recent file instead of stale/global vector data.
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
            "answer": result.get("answer", "")
        })
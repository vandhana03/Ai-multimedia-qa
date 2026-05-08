from pathlib import Path

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .models import UploadedFile
from .utils.pdf_parser import extract_pdf_text
from .utils.transcriber import transcribe_file
from chatbot.utils.vector_store import create_vector_store
# from rest_framework.permissions import IsAuthenticated

class UploadFileView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self,request):
        file = request.FILES.get('file')
        title = request.data.get('title', '').strip()

        if not file:
            return Response(
                {"error": "file is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not title:
            return Response(
                {"error": "title is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        extension = Path(file.name).suffix.lower().replace(".", "")

        file_type = None

        if extension in ['pdf']:
            file_type = 'pdf'
        elif extension in ['mp3', 'wav', 'm4a']:
            file_type = 'audio'
        elif extension in ['mp4', 'mov', 'webm', 'mkv']:
            file_type = 'video'
        else:
            return Response(
                {"error": f"unsupported file type: .{extension}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded = UploadedFile.objects.create(
            # user=request.user,
            title=title,
            file=file,
            file_type=file_type
        )

        path = uploaded.file.path

        if file_type == 'pdf':
            text = extract_pdf_text(path)

        else:
            result = transcribe_file(path)
            text = result['text']

        uploaded.extracted_text = text
        uploaded.save()
        create_vector_store(text)

        return Response({
            "message": "uploaded successfully",
            "file_type": uploaded.file_type,
            "file_url": request.build_absolute_uri(uploaded.file.url),
            "title": uploaded.title,
        })
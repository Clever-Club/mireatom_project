from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from docx import Document
import json
import re

from library.models import Formula, Variable
from modules.text_assembler import replace_formulas_with_math_objects



class DocsCreationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        input_text = json.loads(request.body).get('text', None)
        if not input_text:
            return Response({'error': 'Argument "text" required'}, status=status.HTTP_400_BAD_REQUEST)
        formulas = {}
        for i in re.findall(r'%<([^>]+)>%', input_text):
            formulas[i] = get_object_or_404(Formula, pk=int(i)).value
        doc = Document()

        replace_formulas_with_math_objects(doc, input_text, formulas)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="api_documentation.docx"'

        doc.save(response)

        return response
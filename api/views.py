import xml.etree.ElementTree as ET

from django.db import connection
from rest_framework import filters
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser

from api.models import Mark, Model
from api.serializers import MarkSerializer, ModelSerializer


def clean_table():
    Mark.objects.all().delete()
    Model.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'api_model';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'api_mark';")


class CustomXMLParser(XMLParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', 'utf-8')

        try:
            tree = ET.parse(stream)
        except ET.ParseError as exc:
            raise ParseError('XML parse error - %s' % str(exc))

        root = tree.getroot()
        marks = root.findall('mark')

        data = []
        for mark in marks:
            mark_name = mark.get('name')
            folders = mark.findall('folder')
            folder_names = [folder.get('name') for folder in folders]

            processed_names = []
            for name in folder_names:
                name_parts = name.split(',', 1)
                if len(name_parts) > 0:
                    left_part = name_parts[0].strip()
                    processed_names.append({"name": left_part})
                else:
                    processed_names.append({"name": name})

            data.append({'name': mark_name, 'models': processed_names})

        return data


class UpdateCatalog(APIView):
    parser_classes = [CustomXMLParser]

    def post(self, request):
        clean_table()
        serializer = MarkSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Data processed from XML")
        return Response(serializer.errors, status=400)


class ModelsList(generics.ListAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('mark__name',)
    ordering = ('birth_year',)

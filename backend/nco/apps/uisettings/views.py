from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import (
    UiSection,
    UiField,
)
from .serializers import (
    UiSectionSerializer,
    UiFieldSerializer,
    ReorderSerializer,
)
from .permissions import ReadAnyWriteStaff

# Create your views here.


class UiSectionViewSet(ModelViewSet):
    permission_classes = [ReadAnyWriteStaff]
    serializer_class = UiSectionSerializer
    lookup_field = 'section_id'
    pagination_class = None

    def get_queryset(self):
        query = UiSection.objects.prefetch_related('fields')
        page_key = self.request.query_params.get('page_key')
        if page_key:
            query = query.filter(page_key=page_key)
        return query

    def perform_create(self, serializer):
        serializer.save(update_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(update_user=self.request.user)

    @action(detail=False, methods=['post'], url_path='reorder')
    def reorder(self, request):
        """body: [{"id": <section_id>, "display_order": <int>}, ...]"""
        serializer = ReorderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            for row in serializer.validated_data:
                UiSection.objects.filter(section_id=row['id']).update(
                    display_order=row['display_order']
                )
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)


class UiFieldViewSet(ModelViewSet):
    permission_classes = [ReadAnyWriteStaff]
    serializer_class = UiFieldSerializer
    lookup_field = 'field_id'
    pagination_class = None

    def get_queryset(self):
        query = UiField.objects.select_related('section')
        section_id = self.request.query_params.get('section')
        page_key = self.request.query_params.get('page_key')
        if section_id:
            query = query.filter(section__section_id=section_id)
        if page_key:
            query = query.filter(section__page_key=page_key)
        return query

    def perform_create(self, serializer):
        serializer.save(update_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(update_user=self.request.user)

    @action(detail=False, methods=['post'], url_path='reorder')
    def reorder(self, request):
        """body: [{"id": <field_id>, "display_order": <int>}, ...]"""
        serializer = ReorderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            for row in serializer.validated_data:
                UiField.objects.filter(field_id=row['id']).update(
                    display_order=row['display_order']
                )
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)


class UiPageConfigView(APIView):
    """the whole layout of one page, ready to be applied by the front end"""

    permission_classes = [ReadAnyWriteStaff]

    def get(self, request, page_key):
        sections = (
            UiSection.objects.filter(page_key=page_key)
            .prefetch_related('fields')
        )
        return Response({
            'page_key': page_key,
            'sections': UiSectionSerializer(sections, many=True).data,
        })

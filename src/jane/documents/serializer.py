# -*- coding: utf-8 -*-

from rest_framework import serializers, pagination
from rest_framework.reverse import reverse
from rest_framework_gis.serializers import GeoModelSerializer

from jane.documents import models



class DocumentTypeHyperlinkedIdentifyField(
        serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if obj.pk is None:
            return None

        lookup_value = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_url_kwarg: lookup_value}

        # Deal with documents as well as indices.
        if hasattr(obj, "document_type"):
            kwargs["document_type"] = obj.document_type.name
        else:
            kwargs["document_type"] = obj.document.document_type.name

        url = self.reverse(view_name, kwargs=kwargs, request=request,
                           format=format)
        return url


class DocumentSerializer(serializers.ModelSerializer):
    data_url = serializers.HyperlinkedIdentityField(
        view_name="document_data", lookup_field="pk")

    url = DocumentTypeHyperlinkedIdentifyField(
        view_name='rest_documents-detail',
        lookup_field="pk",
        read_only=True)

    class Meta:
        model = models.Document
        fields = [
            'id',
            'name',
            'url',
            'data_url',
            'document_type',
            'content_type',
            'filesize',
            'sha1',
            'created_at',
            'modified_at',
            'created_by',
            'modified_by'
        ]


class DocumentIndexSerializer(serializers.ModelSerializer):
    url = DocumentTypeHyperlinkedIdentifyField(
        view_name='rest_document_indices-detail',
        lookup_field="pk",
        read_only=True)

    containing_document_url = DocumentTypeHyperlinkedIdentifyField(
        view_name='rest_documents-detail',
        lookup_field="document_id",
        lookup_url_kwarg="pk",
        read_only=True)

    containing_document_data_url = serializers.HyperlinkedIdentityField(
        view_name="document_data", lookup_field="document_id",
        lookup_url_kwarg="pk")


    class Meta:
        model = models.DocumentIndex
        fields = [
            'id',
            'url',
            'containing_document_url',
            'containing_document_data_url',
            'json',
            'geometry',
            'created_at'
        ]


class AttachmentSerializer(serializers.ModelSerializer):

    url = serializers.URLField(source='pk', read_only=True)

    def transform_url(self, obj, value):
        request = self.context.get('request')
        rt_name = self.context.get('resource_type_name')
        index_id = obj.index.pk
        return reverse('attachment_detail', args=[rt_name, index_id, value],
                       request=request)

    class Meta:
        model = models.DocumentIndexAttachment
        fields = ('id', 'url', 'category', 'content_type', 'created_at')


class RecordSerializer(GeoModelSerializer):

    data_url = serializers.HyperlinkedIdentityField(
        view_name="document_data", lookup_field="pk")
    data_content_type = serializers.CharField(source="document.content_type")

    attachments = AttachmentSerializer(many=True)
    indexed_data = serializers.CharField(source="json")
    url = serializers.URLField(source='pk', read_only=True)

    def transform_url(self, obj, value):
        request = self.context.get('request')
        rt_name = self.context.get('resource_type_name')
        return reverse('record_detail', args=[rt_name, value], request=request)

    class Meta:
        model = models.DocumentIndex
        fields = ('id', 'url', 'document', 'data_url',
                  'data_content_type', 'created_at', 'indexed_data',
                  'geometry', 'attachments', 'created_at')


# class PaginatedRecordSerializer(pagination.PaginationSerializer):
#     """
#     Serializes page objects of index querysets.
#     """
#     pages = serializers.Field(source='paginator.num_pages')
#
#     class Meta:
#         object_serializer_class = RecordSerializer

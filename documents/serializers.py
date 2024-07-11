from rest_framework import serializers
from .models import Document, Content

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'user', 'upload_date', 'status']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'document', 'original_content', 'improved_content']

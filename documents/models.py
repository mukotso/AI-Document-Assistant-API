from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    upload_date = models.DateTimeField(auto_now_add=True, db_column='upload_date')
    status = models.CharField(max_length=20, default='uploaded', db_column='status')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'documents'

class Content(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, db_column='document_id')
    original_content = models.TextField(db_column='original_content')
    improved_content = models.TextField(blank=True, null=True, db_column='improved_content')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'contents'

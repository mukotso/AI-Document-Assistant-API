from django.urls import path
from .views import upload_document, get_document, improve_document, update_document_status, get_all_documents, get_statistics

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('documents/<int:id>/', get_document, name='get_document'),
    path('documents/<int:id>/improve/', improve_document, name='improve_document'),
    path('documents/<int:id>/update-status/', update_document_status, name='update_document_status'),
    path('documents/', get_all_documents, name='get_all_documents'),
     path('get_statistics/', get_statistics, name='get_statistics'),
]

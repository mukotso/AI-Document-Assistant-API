from django.urls import path
from .views import upload_document, get_document, improve_document

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('documents/<int:id>/', get_document, name='get_document'),
    path('documents/<int:id>/improve/', improve_document, name='improve_document'),
]

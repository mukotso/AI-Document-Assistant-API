from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Document, Content
from docx import Document as DocxDocument
import PyPDF2
import os
from .nlp_utils import improve_document_content


# maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_document(request):
    user = request.user
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        return Response({"error": "File size exceeds the limit of 10MB"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Extract file name and extension
        file_name = file.name
        file_name, file_extension = os.path.splitext(file_name)
        
        # Create a new document entry with file name
        document = Document.objects.create(
            user=user,
            file_name=file.name  # Save the original file name
        )
        
        # Extract content from file
        original_content = ''
        if file_extension == '.txt':
            original_content = file.read().decode('utf-8')
        elif file_extension == '.docx':
            doc = DocxDocument(file)
            for para in doc.paragraphs:
                original_content += para.text + '\n'
        elif file_extension == '.pdf':
            pdf = PyPDF2.PdfReader(file)
            for page in pdf.pages:
                original_content += page.extract_text() + '\n'
        else:
            return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the content in the database
        Content.objects.create(document=document, original_content=original_content)
        
        # Construct response data
        response_data = {
            "document_id": document.id,
            "file_name": document.file_name,
            "status": document.status,
            "upload_date": document.upload_date.isoformat(), 
            "content": original_content  
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document(request, id):
    try:
        # Retrieve the document by ID
        document = Document.objects.get(id=id)
        # Retrieve the content associated with the document
        content = Content.objects.get(document=document)
        
        # response data
        response_data = {
            "document_id": document.id,
            "file_name": document.file_name,
            "status": document.status,
            "upload_date": document.upload_date.isoformat(),  
            "original_content": content.original_content,
            "improved_content": content.improved_content or ''  
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
    except Content.DoesNotExist:
        return Response({"error": "Content not found for this document"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def improve_document(request, id):
    try:
       
        document = Document.objects.get(id=id)
        
        content = Content.objects.get(document=document)
        
        # NLP
        improved_content, suggestions = improve_document_content(content.original_content)
        
        # Save the improved content back to the database
        content.improved_content = improved_content
        content.suggestions = suggestions
        content.save()
        
        
        response_data = {
            "document_id": document.id,
            "file_name": document.file_name,
            "status": document.status,
            "upload_date": document.upload_date.isoformat(), 
            "original_content": content.original_content,
            "improved_content": content.improved_content,
            "suggestions": suggestions  
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
    except Content.DoesNotExist:
        return Response({"error": "Content not found for this document"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_document_status(request, id):
    try:
        # Retrieve the document by ID
        document = Document.objects.get(id=id)
        
        # Get the new status from the request data
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({"error": "No status provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the document status
        document.status = new_status
        document.save()
        
        
        
        return Response({'message':"Document Status Updated Successfully"}, status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_documents(request):
    try:
        user = request.user
        # Retrieve all documents for the logged-in user
        documents = Document.objects.filter(user=user)
        # Construct the response data
        response_data = []
        for document in documents:
            try:
                # Retrieve the content associated with the document
                content = Content.objects.get(document=document)
                doc_data = {
                    "document_id": document.id,
                    "file_name": document.file_name,
                    "status": document.status,
                    "upload_date": document.upload_date.isoformat(),  
                    "original_content": content.original_content,
                    "improved_content": content.improved_content or ''  
                }
                response_data.append(doc_data)
            except Content.DoesNotExist:
                continue
        
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..serializers import ArticleSerializer
from ..models import Article,ArticleCategory,ArticleSubCategory
from ..utils import save_file_to_folder, file_path_to_binary
import uuid
from ..pagination import CustomPagination
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now as timezone_now
from django.db.models import Q
from PyPDF2 import PdfReader
import os
from django.conf import settings
from ..enums.article_status_enum import ArticleStatus
from django.http import Http404




# Article in the form of pdf's
class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        article_data = request.data.get('article', None)
        category_id = request.data.get('category_id')
        sub_category = request.data.get('sub_category')

        # Validate that the provided category_id and sub_category exist in their respective models
        if category_id:
            if not ArticleCategory.objects.filter(pk=_id).exists():
                return Response({"error": "Invalid category_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        if sub_category:
            if not ArticleSubCategory.objects.filter(pk=_id).exists():
                return Response({"error": "Invalid sub_category"}, status=status.HTTP_400_BAD_REQUEST)

        if article_data and (category_id or sub_category):
            _id = uuid.uuid1()

            # Save paths to the database
            article = Article(
                _id=_id,
                article=article_data,
                category_id=category_id,
                sub_category=sub_category,
                desc=request.data.get('desc', ''),
                created_at=request.data.get('created_at', timezone_now())
            )
            article.save()

            # Serialize the response data
            serializer = self.get_serializer(article)
            response_data = serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='filter-category/(?P<category_id>[^/.]+)')
    def filter_by_category(self, request, category_id=None):
        if not category_id:
            raise ValidationError("Category ID is required")

        articles = Article.objects.filter(
        Q(category_id=category_id) | Q(subcategory_id=category_id)
    )

        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


                


## article to be displayed as text from pdf

# class ArticleView(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     pagination_class = CustomPagination

#     def extract_text_from_pdf(self, pdf_path):
#         """Utility method to extract text from a PDF file."""
#         try:
#             with open(pdf_path, 'rb') as file:
#                 reader = PdfReader(file)
#                 text = ""
#                 for page in reader.pages:
#                     text += page.extract_text()
#             return text
#         except FileNotFoundError:
#             return None

#     def create(self, request, *args, **kwargs):
#         category_id = request.data.get('category_id')
#         sub_category = request.data.get('sub_category')
#         article_file = request.FILES.get('article', None)

#         if category_id and not ArticleCategory.objects.filter(pk=category_id).exists():
#             return Response({"error": "Invalid category_id"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if sub_category and not ArticleSubCategory.objects.filter(pk=sub_category).exists():
#             return Response({"error": "Invalid sub_category"}, status=status.HTTP_400_BAD_REQUEST)

#         if article_file and (category_id or sub_category):
#             _id = uuid.uuid4()
#             pdf_directory = os.path.join(settings.FILE_PATH, 'articles', str(_id))
#             os.makedirs(pdf_directory, exist_ok=True)
#             pdf_path = os.path.join(pdf_directory, article_file.name)

#             with open(pdf_path, 'wb') as pdf_file:
#                 for chunk in article_file.chunks():
#                     pdf_file.write(chunk)

#             article = Article(
#                 _id=_id,
#                 article=pdf_path,
#                 category_id_id=category_id,
#                 subcategory_id_id=sub_category,
#                 status=request.data.get('status', ArticleStatus.PENDING.value),
#                 created_at=request.data.get('created_at', timezone_now())
#             )
#             article.save()

#             serializer = self.get_serializer(article)
#             response_data = serializer.data

#             return Response(response_data, status=status.HTTP_201_CREATED)
        
#         return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         response_data = serializer.data

#         # Extract text from the PDF on demand
#         pdf_path = os.path.join(settings.FILE_URL, instance.article)
#         extracted_text = self.extract_text_from_pdf(pdf_path)
#         if extracted_text is None:
#             raise Http404("File not found or error reading the file.")
        
#         response_data['extracted_text'] = extracted_text

#         return Response(response_data)

#     @action(detail=False, methods=['get'], url_path='filter-category/(?P<category_id>[^/.]+)')
#     def filter_by_category(self, request, category_id=None):
#         if not category_id:
#             raise ValidationError("Category ID is required")

#         articles = Article.objects.filter(
#             Q(category_id=category_id) | Q(subcategory_id=category_id)
#         )

#         page = self.paginate_queryset(articles)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(articles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
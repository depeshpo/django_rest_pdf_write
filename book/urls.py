from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, PDFWrite, CSVWrite

router = DefaultRouter()
router.register('api/books', BookViewSet, base_name='books')

urlpatterns = [
    path('', include(router.urls)),
    path('api/book-invoice-pdf', PDFWrite.as_view()),
    path('api/books-csv', CSVWrite.as_view())
]

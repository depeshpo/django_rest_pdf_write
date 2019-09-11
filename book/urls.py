from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, PDFWrite, CSVWrite, MyPDFWrite, TicketPDF, ReportPDF, BooksRecordExcel

router = DefaultRouter()
router.register('api/books', BookViewSet, base_name='books')

urlpatterns = [
    path('', include(router.urls)),
    path('api/book-invoice-pdf/', PDFWrite.as_view()),
    path('api/books-csv/', CSVWrite.as_view()),
    path('api/write-book-pdf/', MyPDFWrite.as_view()),
    path('api/ticket-pdf/', TicketPDF.as_view()),
    path('api/report-pdf/', ReportPDF.as_view()),
    path('api/books-excel/', BooksRecordExcel.as_view())
]

import datetime
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from book.models import Book
from book.pdf import PDFTemplateView
from book.serializers import BookReadSerializer, BookWriteSerializer
from book.utils import render_to_pdf, export_to_csv, export_to_excel


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['author', 'name', 'detail__detail']
    ordering_fields = ['author', 'name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookReadSerializer
        return BookWriteSerializer


class PDFWrite(APIView):
    def get(self, request):
        try:
            book = Book.objects.all().latest('created')
            if book:
                data = {
                    'today': datetime.date.today(),
                    'author': book.author,
                    'book_name': book.name,
                    'book_detail': book.detail.detail,
                    'book_created_date': book.created
                }
                pdf = render_to_pdf('pdf/book-invoice.html', data)
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Invoice_%s.pdf" % '12332'
                    content = "inline; filename=%s" % filename
                    response['Content-Disposition'] = content
                    return response
        except:
            return Response({
                'message': "Can't create pdf"
            }, status=status.HTTP_200_OK)


class CSVWrite(APIView):
    @staticmethod
    def get(request):
        try:
            fields = ['author', 'detail']
            books = Book.objects.all()
            csv_file_name = 'author.csv'
            data = export_to_csv(queryset=books, fields=fields, file_name=csv_file_name)
            return HttpResponse(data, content_type='text/csv')
        except Exception as e:
            print(e)
            return Response({
                'message': 'Can not create CSV file'
            }, status=status.HTTP_200_OK)


class MyPDFWrite(PDFTemplateView):
    template_name = "my_folder/book.html"
    filename = 'book-invoice.html'

    def get_context_data(self, **kwargs):
        book = Book.objects.all().latest('created')
        context = super(MyPDFWrite, self).get_context_data(**kwargs)
        context['books'] = book
        return context


class TicketPDF(PDFTemplateView):
    template_name = 'my_folder/ticket/ticket.html'
    filename = 'ticket.pdf'


class ReportPDF(PDFTemplateView):
    template_name = 'my_folder/report/report.html'
    filename = 'report.pdf'


class BooksRecordExcel(APIView):
    def get(self, request):
        try:
            books = Book.objects.all()
            file_name = 'books-excel.xlsx'
            field_names = ['ID', 'Name', 'Author', 'Created at', 'Detail']
            kwargs = {"file_name": file_name, "field_names": field_names}
            data = export_to_excel(books, **kwargs)
            return data
        except:
            return Response({
                'message': 'Can not create Excel File'
            }, status=status.HTTP_200_OK)

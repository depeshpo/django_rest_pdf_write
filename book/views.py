import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from weasyprint import HTML, CSS

from book.models import Book
from book.pdf import PDFTemplateResponseMixin
from book.serializers import BookReadSerializer, BookWriteSerializer
from book.utils import render_to_pdf, populate_from_csv


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()

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
            # fields = ['author']
            # books = Book.objects.values_list(fields)
            books = Book.objects.all()
            csv_file_name = 'author.csv'
            data = populate_from_csv(books, csv_file_name)
            return HttpResponse(data, content_type='text/csv')
        except:
            return Response({
                'message': 'Can not create CSV file'
            }, status=status.HTTP_200_OK)


class MyPDFWrite(TemplateView, PDFTemplateResponseMixin):
    template_name = "my_folder/book.html"
    filename = 'book-invoice.html'

    def get_context_data(self, **kwargs):
        book = Book.objects.all().latest('created')
        context = super(MyPDFWrite, self).get_context_data(**kwargs)
        context['books'] = book
        return context


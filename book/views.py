import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookReadSerializer, BookWriteSerializer
from book.utils import render_to_pdf


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookReadSerializer
        return BookWriteSerializer


class PDFWrite(APIView):

    def get(self, request):
        try:
            book = Book.objects.filter(author='Nitesh Paudel').latest('created')
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
                'message': 'Book matching author not found'
            }, status=status.HTTP_200_OK)

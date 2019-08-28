from rest_framework.viewsets import ModelViewSet

from book.models import Book
from book.serializers import BookReadSerializer, BookWriteSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookReadSerializer
        return BookWriteSerializer

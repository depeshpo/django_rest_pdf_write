from rest_framework import serializers

from book.models import Book, BookDetail


class BookDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = BookDetail
        fields = ('id', 'detail')


class BookReadSerializer(serializers.ModelSerializer):
    detail = BookDetailSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'author', 'name', 'detail', 'created')


class BookWriteSerializer(serializers.ModelSerializer):
    detail = BookDetailSerializer()

    class Meta:
        model = Book
        fields = ('id', 'author', 'name', 'detail', 'created')

    def create(self, validated_data):
        detail = validated_data.pop('detail')
        book = Book.objects.update_or_create(**validated_data)
        BookDetail.objects.create(book=book[0], **detail)
        return book[0]

    def update(self, instance, validated_data):
        detail = validated_data.pop('detail')
        instance.author = validated_data.get('author', instance.author)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        book_detail = BookDetail.objects.get(book=instance)
        book_detail.detail = detail.get('detail', book_detail.detail)
        book_detail.save()

        return instance

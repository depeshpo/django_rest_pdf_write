from django.db import models


class Book(models.Model):
    author = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class BookDetail(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='detail')
    detail = models.TextField()

    def __str__(self):
        return self.book.name

import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_pdf_write.settings')

import django

django.setup()

from faker import Faker

from book.models import Book, BookDetail

faker = Faker()


def populate_book(N):
    for n in range(N):
        print('*'*n)
        fake_author = faker.name()
        fake_name = faker.sentence(nb_words=4)
        Book.objects.create(author=fake_author, name=fake_name)


def populate_book_detail():
    books = Book.objects.all()
    fake_detail = faker.text(max_nb_chars=200)
    for book in books:
        print('*')
        BookDetail.objects.create(book=book, detail=fake_detail)


if __name__ == '__main__':
    if populate_book:
        print("------------------------------------------------------")
        print("Populating Book ...")
        populate_book(30)
        print("Populating Book completed")

    if populate_book_detail:
        print("-------------------------------------------------------")
        print("Populating book detail ...")
        populate_book_detail()
        print("Populating book detail completed")

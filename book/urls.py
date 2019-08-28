from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book.views import BookViewSet

router = DefaultRouter()
router.register('api/books', BookViewSet, base_name='books')

urlpatterns = [
    path('', include(router.urls))
]

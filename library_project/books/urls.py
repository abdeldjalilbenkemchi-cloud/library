
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookDetailView, BookListCreateView

# router = DefaultRouter()
# router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('books/', BookListCreateView.as_view(),name='book_list_create'),
    path('books/<int:pk>/', BookDetailView.as_view(),name='book_Detail')

]
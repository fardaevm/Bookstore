from django.urls import path
from .views import BooksListView, BooksDetailView

urlpatterns = [
    path('', BooksListView.as_view(), name='book_list'),
    path('<uuid:pk>/', BooksDetailView.as_view(), name='book_detail'),
]
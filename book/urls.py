from django.urls import path, include
from .views import BookDetailsView,borrow_book,BorrowBookListView,return_book
urlpatterns = [
    path('details/<int:id>', BookDetailsView.as_view(), name='book_detail'),
    path('borrow_book/<int:id>', borrow_book, name='borrow_book'),
    path('borrow_book_lists/', BorrowBookListView.as_view(), name='borrow_book_lists'),
    path('borrow_book_return/<int:id>', return_book, name='borrow_book_return'),
]
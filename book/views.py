from django.shortcuts import render, redirect, get_object_or_404
from .models import BookModel
from django.views.generic import DetailView, View, ListView
from .forms import ReviewForm
from user.models import BorrowHistory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from book.models import BookModel
from user.models import BorrowHistory
from django.utils import timezone
# Create your views here.


class BookDetailsView(DetailView):
    model = BookModel
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        bookmodel = self.get_object()
        if review_form.is_valid():
            new_comment = review_form.save(commit=False)
            new_comment.book = bookmodel
            new_comment.user = request.user
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.review.all()
        review_form = ReviewForm()
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context


def borrow_book(reuqest, id):
    book_model = BookModel.objects.get(pk=id)
    acc = reuqest.user.account
    if acc.balance > book_model.price:
        acc.balance -= book_model.price
        acc.save(
            update_fields=[
                'balance'
            ]
        )
        history = BorrowHistory(
            book=book_model, user=acc)
        history.save()
    else:
        messages.error(reuqest, 'You do not have sufficient balance')
        return redirect('book_detail', id=id)
    return redirect('book_detail', id=id)


def return_book(request, id):
    borrow_book = BorrowHistory.objects.get(pk=id)
    account = request.user.account
    account.balance += borrow_book.user.balance
    account.save()
    borrow_book.delete()
    return redirect('borrow_book_lists')


class BorrowBookListView(LoginRequiredMixin, ListView):
    model = BorrowHistory
    template_name = 'borrow_book.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = BorrowHistory.objects.filter(user__user_id=user_id)
        return queryset

from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Transaction
from django.views.generic import CreateView, DetailView, View, ListView
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, EmailMessage
from .forms import DepositForm
from book.models import BookModel
from user.models import BorrowHistory
# Create your views here.



class BookBorrowView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        book = get_object_or_404(BookModel, id=id)
        user = self.request.user
        if user.account.balance > book.price:
            user.account.balance -= book.borrowed_price
            messages.success(request, 'book borrowed successful')
            user.account.save(update_fields=['balance'])
            BorrowHistory.objects.create(
                book=book,
                user=request.user.account,
                borrow_date=timezone.now(),
            )
            # send_email(user,book.borrowed_price, 'borrow', 'Book Borrow Message','transactions/email_template.html')
            return redirect('borrow_book_lists')
        else:
            messages.error(request, 'Insufficient balance to borrow the book')
            return redirect('home')


class UserDepositView(CreateView):
    template_name = 'deposit.html'
    model = Transaction
    form_class = DepositForm

    def form_valid(self, form):
        account = self.request.user.account
        amount = form.cleaned_data.get('amount')
        account.balance += amount
        account.save(update_fields=['balance'])
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.amount = amount
        transaction.save()
        email_subject = "Money Deposited."
        email_body = render_to_string("deposite_email.html",{'user':self.request.user,'amount':amount})
        email = EmailMultiAlternatives(email_subject,'',to=[self.request.user.email])
        email.attach_alternative(email_body,'text/html')
        email.send()
        messages.success(
            self.request, f'your account has been successfully depostied {amount} tk')
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Depsoit Money"
        return context


@login_required
def deposit(request):
    if request.method == 'POST':
        deposit_amount = request.POST.get('deposit_amount')

        if isinstance(deposit_amount, int):

            if deposit_amount <= 0:

                error_message = "Deposit amount must be a positive value."
                return render(request, 'deposit.html', {'error_message': error_message})
            user = request.user
            account = user.account
            account.balance += deposit_amount
            account.save()
            
            return redirect('success_page')
        else:
            error_message = "Invalid deposit amount. Please enter a valid number."
            return render(request, 'deposit.html', {'error_message': error_message})

    return render(request, 'deposit.html')




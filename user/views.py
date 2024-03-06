from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserUpdateForm

# class based views imports

from django.contrib.auth.decorators import login_required
from django.views.generic import FormView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# views here.

def send_email(user,amount,email_type,mail_subject,template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
        'type': email_type,
    })
    from_email = "BOOK SHELF <delwarjnu24@gmail.com>"
    send_email = EmailMultiAlternatives(mail_subject, '', to=[user.email], from_email=from_email, reply_to=[from_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class UserRegistrationView(FormView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'user created successful.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Some field is inputed wrongly.')
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        messages.success(self.request, 'User logged in ')
        return reverse_lazy('home')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')


class UserUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Profile updated successfully done')
            return redirect('home') 
        return render(request, self.template_name, {'form': form})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # send_email(self.request.user, "", 'pass_change',  'Password Change Success Message', 'transactions/email_template.html')
        messages.success(self.request, 'Password changed successfully done')
        return super().form_valid(form)
# imports
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserAccount

# views
class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    mobile_no = forms.IntegerField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','gender','mobile_no', 'email', 'birth_date', 'password1', 'password2']
        
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save() 
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            mobile_no = self.cleaned_data.get('mobile_no')
            
            UserAccount.objects.create(
                user = our_user,
                gender = gender,
                account_no = 100+ our_user.id,
                birth_date =birth_date,
                mobile_no = mobile_no,
            )
        return our_user
    


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance:
            try:
                user_account = self.instance.account
                
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user)  
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()
        return user
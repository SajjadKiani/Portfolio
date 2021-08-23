from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm

class AddAssetForm(forms.Form):

    # users = User.objects.all()
    # list = []

    # for u in users:
    #     list.append( (u , u.username) )

    # user = forms.ChoiceField(choices = tuple(list))
    coin_name = forms.CharField(max_length=100)
    amount = forms.IntegerField()
    time = forms.DateField()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30 , help_text='Optional.')
    last_name = forms.CharField(max_length=30 , help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
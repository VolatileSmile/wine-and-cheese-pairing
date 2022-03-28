from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'avatar', 'bio', 'age', 'birthday',)

# class EditProfileForm(UserChangeForm):
#     user = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     bio = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     age = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))

    # user = forms.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # #slug = models.SlugField(max_length = 250, null = True, blank = True)
    # avatar = forms.CharField(max_length=20, blank=True, null=True) #holy shit i did it boys
    # bio = forms.TextField(max_length=500, blank=True)
    # age = forms.CharField(max_length=3, blank=True)
    # birth_date = forms.DateField(null=True, blank=True)

    # class Meta:
    #     model = User
    #     fields = ('user', 'bio', 'age', 'birth_date',)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['user', 'bio', 'age', 'birth_date']


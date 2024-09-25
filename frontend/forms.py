from django import forms
from .models import Product, Auction, Comment
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['starting_price', 'bid_end_time']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} estrella{"s" if i > 1 else ""}') for i in range(1, 6)]),
        }

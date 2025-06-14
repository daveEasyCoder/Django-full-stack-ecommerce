from .models import Product, Category, Cart
from django import forms
from django.contrib.auth.models import User


class userLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']

        widgets = {
            'username':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter First name'}),
            'email':forms.EmailInput(attrs={'class':'text-input','placeholder':'Enter your email'}),
            'password':forms.PasswordInput(attrs={'class':'text-input','placeholder':'Enter password'}),
        }
        help_texts = {
            'username': None,
        }
       


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6,'placeholder':'Enter Description...'}),
            'price': forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Price'}),
            'category': forms.Select(attrs={'class':'form-control','placeholder':'Enter Price'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Choose a Category" 


        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

        labels = {
            'CategoryImage':'Image',
        }

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Category Name'})
        }
        
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('__all__')
        
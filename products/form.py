from distutils.log import error
from tkinter import Widget
from . models import *
from django import forms

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields="__all__"
        labels={"brand_name":"Brand Name","brand_logo":"Brand Logo","reg_date":"Registration Date"}
        widgets={"brand_name":forms.TextInput(attrs={'placeholder':"Brand Name"}),
        "reg_date":forms.DateTimeInput(format="%Y-%m-%d %H:%M:%S",
        attrs={'type':"date",'placeholder':"dd-mm-yyyy"})}


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"

class UserForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=["user_name","email","password","mobile","address"]
        widgets={"password":forms.TextInput(attrs={'type':"password"})}
    


        

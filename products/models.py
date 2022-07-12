from cgi import print_exception
from pyexpat import model
from django.db import models
import datetime
# Create your models here.
class Brand(models.Model):
    brand_name=models.CharField(max_length=50)
    brand_logo=models.ImageField(upload_to="media/brand")
    reg_date=models.DateTimeField()

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name=models.CharField(max_length=50, default="Men")
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_price=models.IntegerField()
    product_description=models.TextField()
    product_logo=models.ImageField(upload_to="products")
    product_size=models.CharField(max_length=50)
    product_quantity=models.IntegerField()
    product_brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    product_category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.product_name

class MyUser(models.Model):
    user_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    mobile=models.BigIntegerField()
    start_date=models.DateField(default=datetime.datetime.now())
    address=models.TextField()
    def __str__(self):
        return self.user_name

class Cart(models.Model):
    product_id=models.IntegerField(default=-1)
    item_name=models.CharField(max_length=50)
    quanitity=models.IntegerField()
    price=models.IntegerField()
    user_email=models.EmailField(max_length=50)
    
    def __str__(self):
        return self.item_name
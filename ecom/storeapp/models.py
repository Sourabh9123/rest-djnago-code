from django.db import models
import uuid
from account.models import User

from django.contrib.auth import get_user_model

User = get_user_model()






class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200, unique=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discription = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name
    

PRODUCT_SIZE = (
    ('S','Small'),
    ('M', "Medium"),
    ('L', 'Large'),
)



class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    discription = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")
    price = models.DecimalField(max_digits=100, decimal_places=2)
    image = models.ImageField(upload_to='products/images', default='')
    product_quantity = models.PositiveIntegerField(default=0)
    avalible_sizes = models.CharField(max_length=200, choices=PRODUCT_SIZE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name
    
    def product_attributes_data(self):
        product_attributes = ProductAttribute.objects.filter(product=self.id)
        return product_attributes






class SizeAttribute(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    size = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.size
    

class ColorAttribute(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.color
    


class ProductAttribute(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeAttribute, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorAttribute, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.product}---{self.size}"
    
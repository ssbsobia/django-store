# from django.db import models

# Create your models here.
from django.db import models

from config import settings

user= settings.AUTH_USER_MODEL
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    # this field allows us to create a hierarchy of categories and subcategories  
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    purchased_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    description = models.TextField(blank=True, null=True)

    stock = models.PositiveIntegerField(default=0)

    ram = models.CharField(max_length=20, blank=True, null=True)
    storage = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    # In a real application, you would likely want to use a more robust solution for handling product images, such as a separate model for product images or integration with a cloud storage service.
    image = models.ImageField(upload_to='products/product_img/%Y/%m/%d/', null=True, blank=True)

    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True) 
    created_by = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_products')



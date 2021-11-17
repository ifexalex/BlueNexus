from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from category.models import Category
from vendor.models import Vendor

# Create your models here.

class Product(models.Model):
    
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(_("product slug"), unique=True)
    description = models.TextField(max_length= 500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField(_("stock count"))
    is_available  = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    #vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return str(self.product_name)
    
    def get_url(self): 
        return reverse('product_detail', args=[self.category.slug, self.slug])
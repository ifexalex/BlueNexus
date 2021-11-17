from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.


class Vendor(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100, unique=True)
    store_image = models.ImageField(upload_to='photos/vendors', blank=True)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now =True)
    is_active = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.store_name)
    
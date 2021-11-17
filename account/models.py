from django.db import models
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin, UserManager

# Create your models here.


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, first_name, last_name,password, **extra_fields):
        """
        Create a new user and save the user's information with the given email, first_name, surname, phone and password
        """
        
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email).lower()
        user = self.model(email = email, username=username ,first_name=first_name, last_name=last_name,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    
    def create_user(self, email, username ,first_name, last_name,password, **extra_fields):
        extra_fields.setdefault('is_staff',False )
        extra_fields.setdefault('is_superuser',False)
        
        
        return self._create_user(email,username, first_name, last_name,password, **extra_fields )
    
    def create_vendor(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_vendor', True)
        
        if extra_fields.get('is_vendor') is not True:
            raise ValueError('Vendor must have is_vendor = True')
        if extra_fields.get('is_superuser') is True:
            raise ValueError('Vendor cannot have is_superuser = True')
        
        return self._create_user(email, first_name, last_name,password, **extra_fields)
        
    
    def create_superuser(self, email, username=None, first_name=None, last_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_vendor', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self._create_user(email, username, first_name, last_name,password, **extra_fields)
    
    
            
        

class User(AbstractUser, PermissionsMixin):
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists. Try again"),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=50)
    
    
    
    
    # required Feilds
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_('Designates whether the user can log into this superadmin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    is_vendor = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 
    ]
    
    objects = MyUserManager()
    
    


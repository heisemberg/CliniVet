from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given username, email, first name, last name and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):      
        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Username', max_length=15, unique=True)
    password = models.CharField('Password', max_length=256)
    email = models.EmailField('Email', max_length=100)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    is_active = models.BooleanField('Is Active', default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Agregado para que el usuario pueda ser parte del staff
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    last_login = models.DateTimeField('Last Login', auto_now=True)
    last_change_date = models.DateTimeField('Last Change Date', auto_now=True)

    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a email address')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=128, unique=True)
    #first_name = models.CharField(max_length=50, blank=True)
    #last_name = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50, unique=True)
    twitter_url = models.CharField(max_length=100, blank=True)
    intro_text = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'user'
        swappable = 'AUTH_USER_MODEL'


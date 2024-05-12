
from email.policy import default
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid 
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


class UserManager(BaseUserManager):
  def create_user(self, email, name,  password=None, user_type=None  , auth_provider=None , auth_token=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
        raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          user_type=user_type,
          auth_provider=auth_provider,
          auth_token=auth_token,
        #   terms_conditions=terms_conditions,
      )
      user.username=user.email
      user.code=uuid.uuid4().hex[:6].upper()
      user.set_password(password)
      user.save(using=self._db)
      return user


  

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    id=models.AutoField(primary_key=True)
    code=models.CharField(max_length=24)
    name=models.CharField(max_length=256)
    username=models.CharField(max_length=256)
    password=models.CharField(max_length=256, default="" ,  blank = True)
    phone = models.IntegerField( default="", blank=True, null=True)
    avatar=models.CharField(max_length=1024)
    remember_token=models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_token =  models.CharField(max_length=256,default="" ,  blank = True)
    auth_provider = models.CharField(max_length=255, default= "" ,   blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    terms_conditions = models.BooleanField(default=True)
    login_mode = models.CharField(max_length=256)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
        
    def set_auth_token(self, token):
        self.auth_token = token
        self.save()

    def set_auth_provider(self, token):
        self.auth_provider = token
        self.save()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
        
class Otp(models.Model):
    id=models.AutoField(primary_key=True)
    code=models.CharField(max_length=24)
    email = models.EmailField(max_length=255)
    otp=models.CharField(max_length=6)
    medium = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Student(models.Model):
    id=models.AutoField(primary_key=True)
    code=models.CharField(max_length=24)      
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_profile', null=True)
    name = models.CharField(max_length=255)
    bio = models.CharField(max_length=24)
    education = models.CharField(max_length=24)
    interests = models.CharField(max_length=24)
    avatar=models.FileField(upload_to="profile/")
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


# class FCMToken(models.Model):
#     id=models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     code=models.CharField(max_length=24)
#     fcm_token = models.CharField(max_length=4048)
#     created_at =models.DateTimeField(auto_now_add=True)
#     status=models.CharField(max_length=200 , default="")



class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=4048)
    user = models.IntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    created = models.DateTimeField(auto_now_add=True)
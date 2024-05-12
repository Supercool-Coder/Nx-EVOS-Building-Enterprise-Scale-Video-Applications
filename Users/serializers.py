from datetime import date
from email.policy import default
# from importlib.metadata import requires
from rest_framework import serializers
from Users.models import User , Otp , Student , Token
import logging
import uuid
from django.contrib.auth.hashers import check_password, is_password_usable, make_password

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
  id=serializers.IntegerField()
  code=serializers.CharField(max_length=200,default="")  
  name=serializers.CharField(max_length=200,default="")  
  email=serializers.CharField(max_length=200,default="")  
  password=serializers.CharField(max_length=200, default="")
  user_type = serializers.CharField(max_length=256,default="") 
  avatar=serializers.CharField(max_length=200, default="")  
  remember_token=serializers.CharField(max_length=200, default="")  
  login_mode = serializers.CharField(max_length=200, default='Email')  
  status = serializers.CharField(max_length=200, default='Active')  
  is_active = serializers.BooleanField(default=True)      
  auth_provider = serializers.CharField(max_length=255,default="Email")  
  auth_token =  serializers.CharField(max_length=255,default="Email") 
  # created_at = serializers.DateTimeField(default=date.today)
  # updated_at = serializers.DateTimeField(default=date.today) 

  class Meta:
    model = User
    # fields= ('__all__')
    fields=['id','code','email', 'name', 'password','avatar','remember_token','login_mode','status','is_active' , 'user_type', 'auth_provider' , 'auth_token']
    extra_kwargs={
      'password':{'write_only':True},
      'id':{'read_only':True}
    }

  def validate(self, attrs):
    name = attrs.get('name')
    password = attrs.get('password')
    # password2 = attrs.get('password2')
    logger.info(attrs)
    # if name != '':
    #   raise serializers.ValidationError("Invalid Username")
    
    # if password != '':
    #   raise serializers.ValidationError("Invalid Password")
    return attrs

class StudentProfileSerializers(serializers.ModelSerializer):
  uuidTemp=uuid.uuid4().hex[:12].upper()
  code=serializers.CharField(default=uuidTemp )
  bio=serializers.CharField(default="My Bio")
  education=serializers.CharField(default="NA")
  interests=serializers.CharField(default="NA")
  avatar=serializers.FileField(default="NA")

  class Meta:
    model = Student
    fields= '__all__'

    def create(self, validated_data):  
        validated_data['code']=uuid.uuid4().hex[:12].upper()
        student_id=validated_data["student"]
        user_instance = User.objects.get(id=student_id)
        return Student.objects.create(**validated_data)



class UserRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=['email', 'name', 'password','auth_provider' , 'auth_token' ]
    extra_kwargs={
      'password':{'write_only':True}
    }

  def validate(self, attrs):
    password = attrs.get('password')
    return attrs
    
  def validate(self, attrs):
    auth_token = attrs.get('auth_token')
    return attrs

  def validate(self, attrs):
    auth_provider = attrs.get('auth_provider')
    return attrs

  def create(self, validate_data):    
    user_instance= User.objects.create_user(**validate_data) 
    uuidTemp=uuid.uuid4().hex[:12].upper()
    return user_instance

class UserLoginSerializers(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=55)
  class Meta:
    model = User
    fields = ['email', 'password']
    

class OtpSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    medium = serializers.CharField(max_length = 20)
    otp=serializers.CharField(default='')
    class Meta:
      model = Otp
      fields = ['email','medium','otp']

    def create(self, validated_data):  
        """ 
        Create and return a new `User` instance, given the validated data. 
        """  
        validated_data['code']=uuid.uuid4().hex[:12].upper()
        validated_data['otp']= uuid.uuid4().hex[:4].upper()
        return Otp.objects.create(**validated_data) 
        
        
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']
    

# User serializer to get Users details in any Serializer
class UserInformationSerializer(serializers.ModelSerializer):
  id= serializers.IntegerField(default=0)
  email=serializers.CharField(default="")
  name=serializers.CharField(default="")
  class Meta:
    model = User
    fields = ['id', 'email', 'name']  
    



class TokensSerializer(serializers.ModelSerializer):
  # print("inside Token serializers for websocket chats")
  key = serializers.CharField(max_length=4048)
  user = serializers.IntegerField(default=0)
  class Meta:
    model = Token
    fields = '__all__'



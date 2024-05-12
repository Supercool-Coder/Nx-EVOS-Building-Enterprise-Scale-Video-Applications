from django.shortcuts import render
# from sre_constants import SUCCESS
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from account.models import User , Otp 
from Users.serializers import UserRegistrationSerializer, UserLoginSerializers, UserSerializer,OtpSerializers, UserProfileSerializer , StudentProfileSerializers , TokensSerializer
from django.contrib.auth import authenticate
# from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from Users.models import User ,  Token ,Student
from Users.models import Otp
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.shortcuts import render
import uuid
from pyfcm import FCMNotification

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data["username"]=serializer.validated_data["email"]
            user = serializer.save()
            print(user)
            uuidTemp=uuid.uuid4().hex[:12].upper()
            #check if Instructor
            # if(user.user_type=="INSTRUCTOR"):     
            #     instructor_profile=Instructor(code=uuidTemp,user=user,bio="NA",education="NA",interests="NA")
            #     instructor_profile.save()
           
            student_profile=Student(code=uuidTemp,user=user,bio="NA",education="NA",interests="NA")
            student_profile.save()

            key = get_tokens_for_user(user)
            if serializer.is_valid():
                # serializer.save()
                # user = User.objects.get()
                data = {
                    "key": key["access"],
                    "user": user.id
                }
                userSerializers = TokensSerializer(data = data)
                if userSerializers.is_valid():
                    userSerializers.save()
            return Response({'status': 'success', 'statusCode': '201', 'message': 'Registration Successfull', 'data': {
            'user': serializer.data,
            # 'token': token
        }

        }, status=status.HTTP_201_CREATED)


        return Response({'status':'already_exists', 'statusCode': '400', 'message': 'Email is already exists','data': None
                
                }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    # renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                key = get_tokens_for_user(user)

                serializers = UserLoginSerializers(user) 
                if serializer.is_valid():
                # serializer.save()
                # user = User.objects.get()
                    token=Token.objects.get(user=user.id)
                    data = {
                        "key": key["access"],
                        "user": user.id
                    }
                    print("The data",data)

                    userSerializers = TokensSerializer(token , data = data, partial = True)
                    print("after serializer :- ", userSerializers)
                    if userSerializers.is_valid():
                        print("The validate data",userSerializers)
                        userSerializers.save()
                        print("data saved")
                # result = None
                # profile= None
                # if user.user_type == "STUDENT":
                #     student_id=user.id
                #     result = Student.objects.get(user=student_id)
                #     profile = StudentProfileSerializers(result) 
                # else:
                #     instructor_id=user.id
                #     result = Instructor.objects.get(user=instructor_id)
                #     profile = InstructorProfileSerializers(result) 

                # serializers.data.pop('password')
                
                        return Response({'status':'success', 'status_code':'202' , 'message':'Signup Success', 'data':{
                            'user': {
                                'name':user.name,
                                'email':user.email,
                                'user_type':user.user_type
                            },
                            # 'profile': profile.data,
                            'token': key
                        }
                
                        }, status=status.HTTP_202_ACCEPTED)
                    return Response({'status':'error', 'status_code':'400' , 'message':'Invalid Credentials Please try again', 'data':None 
                
                        }, status=status.HTTP_202_ACCEPTED)
      

class ForgetPasswordView(APIView):
    def post(self, request, format=None):
        try: 
            serializer = OtpSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                #Generate Email Content
                email_subject="Jobbuzz - Forget Password"
                otp=serializer.data["otp"]                
                email_message="Hi,<br/><br/> OTP -"+otp+" <br/><br/>Regards,<br/>Jobbuzz"
                emailTo=serializer.data["email"]
                #FMC TOKEN NOTIFICATIONS
                # fcm = FCMNotification(api_key="AAAALgps-Tk:APA91bEBDMBuoZl37xI42Bu7yRAbq8G_qomfmHRMXI10RYKm8IgMwma8Il-_4MNuyyVGC9UCL1UFsga6FiPkoA6jtG8vLagKEhbZhrRIkDNg36VLDk7Wsw5XkB85jEeLBMaAWP9AD5vC")
                # fmcList= []
                # users=User.objects.filter(is_active=1)
                # for user in  users:
                #     fmcObj=FCMToken.objects.filter(user_id=user.id)
                #     if len(fmcObj) > 0:
                #         fmcList.append(fmcObj[0].fcm_token)                
                # registration_id =  FCMToken.objects.get(user_id=id)
                message_title = "Password Forget Successfully"
                message_body = "Check your email for otp varification"
                # result = fcm.notify_multiple_devices(registration_ids=fmcList, message_title=message_title, message_body=message_body)
                # res=sendHTMLEmail(emailto=emailTo,subject=email_subject,message=email_message , result=result)  
                # resStr=format('%s'%res)
                return Response ({
                        'status':'SUCCESS',
                        'status_code': 200,
                        'message': 'Please check your email for OTP',
                        'data': { }
                    },status=status.HTTP_200_OK)      
            return Response ({
                'status':'ERROR',
                'status_code': 400,
                'message': 'Invalid Data',
                'data': None
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response ({
                'status':'ERROR',
                'status_code': 500,
                'message': 'Please try again!!! Email server not refuse connection',
                'data': { 
                    otp: serializer.data["otp"] 
                }
            },status=status.HTTP_200_OK)

def sendSimpleEmail(request,emailto):
    res = send_mail("hello paul", "comment tu vas?", "paul@polo.com", [emailto])
    return HttpResponse('%s'%res)

def sendHTMLEmail(emailto, subject, message):
    try:
        email = EmailMessage(subject, message, "no-reply@atoconn.org", [emailto])
        email.content_subtype = "html"
        res = email.send()
        print('%s'%res)
        return res
    except Exception:
        return HttpResponse('Invalid header found.')   

class VerifyOTP(APIView):
    def post(self, request):
            data = request.data
            serializer = OtpSerializers(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']                
                otpObj = Otp.objects.filter(email = email,otp=otp)
                if not otpObj.exists():
                    return Response({
                        'status': 'SUCCESS',
                        'status_code': 400,
                        'message':'Invalid OTP',
                        'data': None
                    })
                
                serializer=UserSerializer(data=data)
                if serializer.is_valid():
                    password = serializer.data['password']
                    print(email)
                    user = User.objects.filter(email = email)
                    if not user.exists():
                        return Response({
                        'status': 'SUCCESS',
                        'status_code': 404,
                        'message':'Invalid User',
                        'data': None
                    })
                    user[0].password = make_password(password)
                    user[0].save()                 
                    return Response({
                        'status': 'SUCCESS',
                        'status_code': 200,
                        'message':'Password change successfully',
                        'data': {}
                    })           
            return Response({
                        'status': 'SUCCESS',
                        'status_code': 401,
                        'message':'Invalid OTP',
                        'data': None
            })
            
class UsersProfileView(APIView):
#   renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        student = UserProfileSerializer(request.user) 
        student_id=student.data["id"] 
        result = Student.objects.get(user=student_id) 
        user = User.objects.get(id=student_id) 
        result.name=user.name
        serializer = StudentProfileSerializers(result) 
        return Response({'status': 'success', 'status_code': '200', 'message': 'Student profile was updated', "data":{"instructor_profile": serializer.data}}, status=200)  


    def post(self, request, format=None):
        student = UserProfileSerializer(request.user) 
        # print(student)
        student_id=student.data["id"] 
        result = Student.objects.get(user=student_id) 
        student_name = request.data.pop("name")[0]
        serializer = StudentProfileSerializers(result,data = request.data ,  partial=True )
        # print(serializer)
        
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=student_id)
            # data = dict()
            data = {
                "name": student_name
            }
            serializer.data["name"]=student_name
            userSerializer = UserRegistrationSerializer(user , data = data , partial=True)
            if userSerializer.is_valid():
                userSerializer.save()
            serializer.data["name"]=student_name
            return Response({'status':'SUCCESS', 'status_code':'200' , 'message':'Profile edit Successfully Success', 'data':{
                'student_profile': {"name":student_name, "bio":serializer.data["bio"],"education":serializer.data["education"], "avatar":serializer.data["avatar"], "interests":serializer.data["interests"]},
            }
            }, status=status.HTTP_202_ACCEPTED)
        return Response({'status':'Error', 'status_code':'400' , 'message':'Invalid Credentials Please try again', 'data':None 
    
            }, status=status.HTTP_202_ACCEPTED)

      

from django.urls import path
from Users.views import UserRegistrationView , UserLoginView, ForgetPasswordView, VerifyOTP, UserProfileView , UsersProfileView
# , InstructorProfileView , FCMTokenView , SocialLoginView


urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('signin/', UserLoginView.as_view(), name='signin'),
    # path('sociallogin/',SocialLoginView.as_view() , name="SocialLoginView"),
    path('forget-password-otp/', ForgetPasswordView.as_view(), name= 'forget-password'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('student/profile/',UsersProfileView.as_view(), name = "Student Profile"),
    # path('instructor/profile/',InstructorProfileView.as_view(), name = "Instructor Profile"),
    # path('fcm_token/',FCMTokenView.as_view() , name='FCMToken'),
    #path('all/fcm_token/',AllFCMToken.as_view(), name='All FCM Tokens')
    
]

from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [

    path('register', UserRegister.as_view(), name='Register'),
    path('login', LoginView.as_view(), name='login'),
    path('NewLoginView', NewLoginView.as_view(), name='NewLoginView'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('changepassword/', ChangePasswordView.as_view() , name="changepassword"),
    path('password-Rest-Email/' , PasswordRestEmail.as_view() , name = "password-Rest-Email"),
    path('password-rest/<uid>/<token>/' ,restpasswordView.as_view()  , name = "password-rest"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),



    # path('healthsafety' , OccupationalHealthSafetyView.as_view() , name = 'Health & safety'),



]

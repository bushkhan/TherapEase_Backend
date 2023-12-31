from django.urls import path, include
from . import views
from knox.views import LogoutView, LogoutAllView


urlpatterns = [
    
    path('create-user/', views.CreateUserAPI.as_view()),
    path('update-user/<int:pk>', views.UpdateUserAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('verify/', views.VerifyOTP.as_view()),
    # path('delete-unverified-user/<int:user_id>/', views.DeleteUnverifiedUserView.as_view()),
    
    
     
]
from django.urls import path, include
from . import views
from knox.views import LogoutView, LogoutAllView


urlpatterns = [
    path('anxiety/', views.AnxietyTestCreateView.as_view()),
    # path('anxiety-details/<int:pk>/', views.AnxietyTestDetailView.as_view()),
    
    
     
]
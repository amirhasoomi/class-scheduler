from django.urls import path
from api import views


urlpatterns = [
    path('schedule', views.SchedulesView.as_view()),
    path('schedule/<int:pk>/', views.ScheduleView.as_view()),
]

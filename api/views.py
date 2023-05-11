from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import ScheduleSerializer
from .models import Schedule
# Create your views here.


class SchedulesView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class ScheduleView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

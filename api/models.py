from django.db import models
from utils.models import CreationMixin
from authentication.models import Profile

# Create your models here.


class Location(CreationMixin):
    name = models.CharField(max_length=10)


class Lesson(CreationMixin):
    name = models.CharField(max_length=128)


class Schedule(CreationMixin):
    name = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    professor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

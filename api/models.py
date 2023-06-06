from django.db import models
from utils.models import CreationMixin
from authentication.models import Profile
from .apps import ApiConfig as conf


class Field(CreationMixin):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, unique=True)


class Plato(CreationMixin):
    building = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    capacity = models.IntegerField()


class Date(CreationMixin):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date_of_week = models.PositiveSmallIntegerField(choices=conf.WEEK_DAYS)


class Lesson(CreationMixin):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=10, unique=True)
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True)
    theory_course = models.IntegerField()
    practical_course = models.IntegerField()


class Exam(CreationMixin):
    name = models.CharField(max_length=128)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=128)


class Schedule(CreationMixin):
    name = models.CharField(max_length=10)
    date = models.ForeignKey(Date, on_delete=models.SET_NULL, null=True)
    Plato = models.ForeignKey(Plato, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    professor = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    capacity = models.IntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

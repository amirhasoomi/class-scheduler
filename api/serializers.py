from rest_framework import serializers
from .models import (Schedule, Plato, Field, Date, Lesson, Exam,)


class FeildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('name', 'code',)


class PLatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = ('name', 'building', 'capacity',)


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ('start_time', 'end_time', 'date_of_week',)


class LessonSerializer(serializers.ModelSerializer):
    field = FeildSerializer()

    class Meta:
        model = Lesson
        fields = ('name', 'code', 'field', 'theory_course', 'practical_course')


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('name', 'date', 'start_time', 'end_time', 'location',)


class ScheduleSerializer(serializers.ModelSerializer):
    date = DateSerializer()
    plato = PLatoSerializer()
    lesson = LessonSerializer()
    exam = ExamSerializer()

    class Meta:
        model = Schedule
        fields = ('name', 'date', 'plato', 'lesson', 'professor', 'capacity', 'exam',)

    def validate(self, attrs):
        # username = attrs['username'].lower()
        # if Profile.objects.filter(username=username).exists():
        #     raise serializers.ValidationError(
        #         dict(username=['username is used before!', ]))
        # if Profile.objects.filter(mobile=attrs['mobile']).exists():
        #     raise serializers.ValidationError(
        #         dict(mobile=['mobile is used before!', ]))
        # if Profile.objects.filter(email=attrs['email']).exists():
        #     raise serializers.ValidationError(
        #         dict(email=['email is used before!', ]))
        return attrs

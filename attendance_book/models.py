from django.db import models

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Subject(models.Model):
    name = models.CharField(max_length=50)


class Student(models.Model):
    student_num = models.CharField(max_length=6, primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    class_num = models.IntegerField()
    

class Teacher(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Timetable(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=50)
    start_period = models.IntegerField()
    end_period = models.IntegerField()


class Attendance(models.Model):
    date = models.DateTimeField()
    period = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
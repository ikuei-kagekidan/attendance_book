from django.db import models

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Student(models.Model):
    student_num = models.CharField(max_length=6, primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    class_num = models.IntegerField()
    def __str__(self):
        return str(self.class_num) + " " + self.person.name

class Teacher(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    def __str__(self):
        return self.person.name


class Timetable(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_period = models.IntegerField()
    period_length = models.IntegerField()
    def __str__(self):
        return str(self.day_of_week) + " " + self.subject.name

class Attendance(models.Model):
    date = models.DateField()
    period = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.IntegerField()
    def __str__(self):
        return str(self.date) + " " + self.student.person.name + " " + str(self.status)

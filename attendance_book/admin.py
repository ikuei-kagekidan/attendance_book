from django.contrib import admin

from .models import Person, Subject, Student, Teacher, Timetable, Attendance

admin.site.register(Person)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Timetable)
admin.site.register(Attendance)
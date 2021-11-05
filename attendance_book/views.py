from django.shortcuts import render

from .models import Attendance, Student

import datetime

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    today = datetime.date.today()
    a = Attendance.objects.filter(date=today)
    s = Student.objects.all()
    if not a:
        return render(request, 'attendance_book/teach_in.html')
    context = {
        "student_list": s,
        "today_attendance_list": a
    }
    return render(request, 'attendance_book/teach_in.html', context)

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

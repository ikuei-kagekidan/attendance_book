from django.shortcuts import render
from django.utils import timezone

from .models import Attendance, Student, Timetable

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    today = timezone.now().date()
    a = Attendance.objects.filter(date=today)
    s = Student.objects.all().order_by("class_num")
    
    subject_list = []
    
    context = {
        "t": today,
        "student_list": s,
        "subject_list": subject_list
    }
    
    #if not subject_list:
    #    today_timetable = Timetable.objects.filter(day_of_week=today.weekday())
    
    return render(request, 'attendance_book/teach_in.html', context)
    
    #if not a:
    #    return render(request, 'attendance_book/teach_in.html')
    #context = {
    #    "student_list": s,
    #    "today_attendance_list": a
    #}
    #return render(request, 'attendance_book/teach_in.html', context)

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

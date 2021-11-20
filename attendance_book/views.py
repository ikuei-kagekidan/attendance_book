from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse

from .models import Attendance, Student, Timetable

import datetime

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    if request.method == 'POST':
        date_string = request.POST["date"]
        date_string = "2021-11-19"
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        week = date.weekday()
        timetable = Timetable.objects.filter(day_of_week=week)
        student = Student.objects.all().order_by("class_num")
        print(timetable)
        for tt in timetable:
            sp = tt.start_period
            pl = tt.period_length
            for s in student:
                for i in range(pl):
                    at = Attendance.objects.create(date=date, period=sp+i, student=s, teacher=tt.teacher, subject=tt.subject, status=0)
                
    
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

#def create_attendance(request):
#    date_string = request.POST["date"]
#    date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
#    week = date.week()
#    timetable = Timetable.objects.filter(day_of_week=week)
#    student = Student.objects.all().order_by("class_num")
#    for tt in timetable:
#        sp = tt.start_period
#        pl = tt.period_length
#        for s in student:
#            for i in range(pl):
#                at = Attendance.objects.creat(date=date, period=sp+i, student=s, teacher=tt.teacher, subject=tt.subject, status=0)
            

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Attendance, Student, Timetable

import datetime
from urllib.parse import urlencode

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    date = timezone.now().date()
    
    if "d" in request.GET:
        date_string = request.GET["d"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    
    attendance = Attendance.objects.filter(date=date)
    student = Student.objects.all().order_by("class_num")
    
    subject_list = []
    
    attendance_status = {}
    for s in student:
        attendance_status[s.student_num] = {}
        for at in attendance.filter(student=s):
            attendance_status[s.student_num][at.period] = at.status
    
    #print(attendance_status)
    
    context = {
        "d": date,
        "student_list": student,
        "subject_list": subject_list,
        "attendance_status": attendance_status
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

def teach_in_post(request):
    if "search-date" in request.POST:
        print("search-date", request.POST)
        date_string = request.POST["date"]
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")
        
    elif "create-timetable" in request.POST:
        print("create-timetable", request.POST)
        date_string = request.POST["date"]
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        if Attendance.objects.filter(date=date):
            #エラー：既にデータが存在している
            print("error")
            return HttpResponseRedirect(f"{url}?{param}")
        week = date.weekday()
        timetable = Timetable.objects.filter(day_of_week=week)
        student = Student.objects.all().order_by("class_num")
        for tt in timetable:
            sp = tt.start_period
            pl = tt.period_length
            for s in student:
                for i in range(pl):
                    at = Attendance.objects.create(date=date, period=sp+i, student=s, teacher=tt.teacher, subject=tt.subject, status=0)
        return HttpResponseRedirect(f"{url}?{param}")
    
    return HttpResponseRedirect(reverse('attendance_book:teacher-input'))

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

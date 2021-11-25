from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Attendance, Student, Timetable

import datetime
from urllib.parse import urlencode
import json

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    date = timezone.now().date()
    
    if "d" in request.GET:
        date_string = request.GET["d"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    
    attendance = Attendance.objects.filter(date=date)
    student = Student.objects.all().order_by("class_num")
    timetable = Timetable.objects.filter(day_of_week=date.weekday()).order_by("start_period")
    
    attendance_status = {}
    for s in student:
        attendance_status[s.student_num] = {}
        for at in attendance.filter(student=s):
            attendance_status[s.student_num][at.period] = at.status
    
    timetable_dict = {}
    for tt in timetable:
        timetable_dict[tt.start_period] = {}
        timetable_dict[tt.start_period]["period_length"] = tt.period_length
        timetable_dict[tt.start_period]["subject"] = tt.subject.name

    context = {
        "d": date,
        "student_list": student,
        "timetable": json.dumps(timetable_dict),
        "attendance_status": json.dumps(attendance_status)
    }
    
    return render(request, 'attendance_book/teach_in.html', context)

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

    elif "update-status" in request.POST:
        date_string = request.POST["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        attendance = Attendance.objects.filter(date=date)
        student = Student.objects.all()
        for key in request.POST:
            if key[:7] == "status-":
                status = int(request.POST[key])
                student_num = key[7:13]
                period = int(key[14])
                s = student.get(pk=student_num)
                at = attendance.get(student=s, period=period)
                if at.status != status:
                    at.status = status
                    at.save()
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")
                
    
    #print(request.POST)
    return HttpResponseRedirect(reverse('attendance_book:teacher-input'))

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

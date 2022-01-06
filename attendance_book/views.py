from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.db.models import Q

from .models import Attendance, Student, Subject, Timetable, Teacher

import datetime
from urllib.parse import urlencode, quote
import json
import csv

def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    date = timezone.now().date()
    
    if "d" in request.GET:
        date_string = request.GET["d"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    
    attendance = Attendance.objects.filter(date=date).order_by("period")
    student = Student.objects.all().order_by("class_num")
    teacher = Teacher.objects.all()
    subject = Subject.objects.all()

    attendance_status = {}
    for s in student:
        attendance_status[s.student_num] = {}
        for at in attendance.filter(student=s):
            attendance_status[s.student_num][at.period] = at.status
    
    timetable = attendance.values("subject", "period").distinct()
    timetable_dict = {}
    sbj_id = -1
    start_period = -1
    period_length = 0
    for tt in timetable:
        if tt["subject"] == sbj_id and tt["period"] == start_period + period_length:
            timetable_dict[start_period]["period_length"] += 1
            period_length += 1
        else:
            sbj_id = tt["subject"]
            start_period = tt["period"]
            period_length = 1
            timetable_dict[start_period] = {}
            timetable_dict[start_period]["period_length"] = 1
            timetable_dict[start_period]["subject"] = Subject.objects.get(pk=sbj_id).name

    context = {
        "d": date,
        "student_list": student,
        "timetable": json.dumps(timetable_dict),
        "attendance_status": json.dumps(attendance_status),
        "teacher_list": teacher,
        "subject_list": subject,
    }
    
    return render(request, 'attendance_book/teach_in.html', context)

def teach_in_post(request):
    if "search-date" in request.POST:
        #print("search-date", request.POST)
        date_string = request.POST["date"]
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")
        
    elif "create-timetable" in request.POST:
        #print("create-timetable", request.POST)
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
        at_obj_list = []
        for tt in timetable:
            sp = tt.start_period
            pl = tt.period_length
            for s in student:
                for i in range(pl):
                    at_obj_list.append(Attendance(date=date, period=sp+i, student=s, teacher=tt.teacher, subject=tt.subject, status=0))
        Attendance.objects.bulk_create(at_obj_list)
        return HttpResponseRedirect(f"{url}?{param}")

    elif "update-status" in request.POST:
        date_string = request.POST["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        attendance = Attendance.objects.filter(date=date)
        student = Student.objects.all()
        at_obj_list = []
        for key in request.POST:
            if key[:7] == "status-":
                status = int(request.POST[key])
                student_num = key[7:13]
                period = int(key[14])
                s = student.get(pk=student_num)
                at = attendance.get(student=s, period=period)
                if at.status != status:
                    at.status = status
                    at_obj_list.append(at)
        Attendance.objects.bulk_update(at_obj_list, ["status"])
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")
   
    elif "delete-sub" in request.POST:
        #print(request.POST)
        date_string = request.POST["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        dbutton = int(request.POST["num_button"])
        dbutton_len = int(request.POST["num_button_len"])
        try:
            q = Q()
            for i in range(dbutton_len):
                q |= Q(period=dbutton+i)
            Attendance.objects.filter(Q(date=date) & q).delete()
        except:
            print("Not Found Date")
        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")

    elif "create-sub" in request.POST:
        sp = int(request.POST["create-sub-sp"])
        pl = int(request.POST["create-sub-pl"])
        t_id = request.POST["create-sub-teacher"]
        s_id = request.POST["create-sub-subject"]
        date_string = request.POST["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

        student = Student.objects.all().order_by("class_num")
        teacher = Teacher.objects.get(pk=t_id)
        subject = Subject.objects.get(pk=s_id)

        at_obj_list = []

        for s in student:
            for i in range(pl):
                at_obj_list.append(Attendance(date=date, period=sp+i, student=s, teacher=teacher, subject=subject, status=0))
        Attendance.objects.bulk_create(at_obj_list)

        url = reverse('attendance_book:teacher-input')
        param = urlencode({"d": date_string})
        return HttpResponseRedirect(f"{url}?{param}")
        
    #print(request.POST)
    # 404 not found
    return HttpResponseRedirect(reverse('attendance_book:teacher-input'))

def teach_agg(request):
    from_date = timezone.now().date()
    to_date = timezone.now().date()
    subject = None
    msg = ""
    istotal = False

    if "from_d" in request.GET:
        from_date_string = request.GET["from_d"]
        from_date = datetime.datetime.strptime(from_date_string, "%Y-%m-%d").date()
    if "to_d" in request.GET:
        to_date_string = request.GET["to_d"]
        to_date = datetime.datetime.strptime(to_date_string, "%Y-%m-%d").date()
    if "sbj" in request.GET:
        subject_pk = request.GET["sbj"]

        if subject_pk == "0":
            istotal = True
        else:
            try:
                subject = Subject.objects.get(pk=subject_pk)
            except Subject.DoesNotExist:
                subject = None
                msg = "That subject dose not exist."

    student = Student.objects.all().order_by("class_num")
    subject_list = Subject.objects.all().order_by("pk")

    if istotal:
        attendance = Attendance.objects.filter(date__gte=from_date, date__lte=to_date)
        date_list = attendance.values("date").distinct()

        attendance_count = {}
        for s in student:
            attendance_count[s.student_num] = {"days_class": 0, "days_absence": 0, "days_late": 0, "days_early": 0}
            at = attendance.filter(student=s)
            for d in date_list:
                a = at.filter(date=d["date"]).order_by("period")

                total_cnt = a.count()
                natd_cnt = a.filter(status=1).count()
                islate = False
                isearly = False
                if a.first().status == 1:
                    for i in a:
                        if i.status == 0:
                            islate = True
                            break
                if a.last().status == 1:
                    for i in a.reverse():
                        if i.status == 0:
                            isearly = True
                            break

                attendance_count[s.student_num]["days_class"] += 1
                attendance_count[s.student_num]["days_absence"] += 1 if natd_cnt == total_cnt else 0
                attendance_count[s.student_num]["days_late"] += 1 if islate else 0
                attendance_count[s.student_num]["days_early"] += 1 if isearly else 0
            attendance_count[s.student_num]["num_class"] = at.exclude(subject=1).count()
            attendance_count[s.student_num]["num_absence"] = at.exclude(subject=1).filter(status=1).count()

        context = {
            "from_d": from_date,
            "to_d": to_date,
            "student_list": student,
            "subject_list": subject_list,
            "attendance_count": json.dumps(attendance_count),
            "msg": msg
        }
        return render(request, 'attendance_book/teach_agg_total.html', context)

    else:
        attendance = Attendance.objects.filter(date__gte=from_date, date__lte=to_date, subject=subject)
        date_list = attendance.values("date").distinct()

        attendance_count = {}
        for s in student:
            attendance_count[s.student_num] = {"days_class": 0, "days_absence": 0, "days_late": 0, "days_early": 0}
            at = attendance.filter(student=s)
            for d in date_list:
                a = at.filter(date=d["date"]).order_by("period")

                total_cnt = a.count()
                natd_cnt = a.filter(status=1).count()
                islate = False
                isearly = False
                if a.first().status == 1:
                    for i in a:
                        if i.status == 0:
                            islate = True
                            break
                if a.last().status == 1:
                    for i in a.reverse():
                        if i.status == 0:
                            isearly = True
                            break

                attendance_count[s.student_num]["days_class"] += 1
                attendance_count[s.student_num]["days_absence"] += 1 if natd_cnt == total_cnt else 0
                attendance_count[s.student_num]["days_late"] += 1 if islate else 0
                attendance_count[s.student_num]["days_early"] += 1 if isearly else 0

            attendance_count[s.student_num]["num_class"] = at.count()
            attendance_count[s.student_num]["num_absence"] = at.filter(status=1).count()

        context = {
            "from_d": from_date,
            "to_d": to_date,
            "student_list": student,
            "subject_list": subject_list,
            "selected_subject": subject,
            "attendance_count": json.dumps(attendance_count),
            "msg": msg
        }
        return render(request, 'attendance_book/teach_agg.html', context)

def teach_agg_post(request):
    if "aggregation" in request.POST:
        #print("aggregation", request.POST)
        from_date_string = request.POST['from-date']
        to_date_string = request.POST['to-date']
        param = {"from_d": from_date_string, "to_d": to_date_string}

        subject_pk = request.POST['subject']
        if subject_pk:
            param["sbj"] = subject_pk

        param = urlencode(param)
        url = reverse('attendance_book:teacher-aggregation')
        return HttpResponseRedirect(f"{url}?{param}")

    print(request.POST)
    return HttpResponseRedirect(reverse('attendance_book:teacher-aggregation'))

def teach_agg_download(request):
    if "from_d" in request.GET and "to_d" in request.GET and "sbj" in request.GET:
        istotal = False

        from_date_string = request.GET["from_d"]
        from_date = datetime.datetime.strptime(from_date_string, "%Y-%m-%d").date()
        to_date_string = request.GET["to_d"]
        to_date = datetime.datetime.strptime(to_date_string, "%Y-%m-%d").date()
        subject_pk = request.GET["sbj"]

        if subject_pk == "0":
            istotal = True
            filename = "全体"
        else:
            try:
                subject = Subject.objects.get(pk=subject_pk)
            except Subject.DoesNotExist:
                # 404 not found
                return render(request, 'attendance_book/teach_agg.html')
            filename = subject.name

        student = Student.objects.all().order_by("class_num")

        filename = quote(filename)
        response = HttpResponse()
        response["Content-Type"] = "text/csv"
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)

        if istotal:
            writer.writerow(["番号", "名前", "授業日数", "欠席日数", "遅刻日数", "早退日数", "授業回数", "欠課数"])
            attendance = Attendance.objects.filter(date__gte=from_date, date__lte=to_date)
            date_list = attendance.values("date").distinct()

            for s in student:
                attendance_count = [0, 0, 0, 0]
                at = attendance.filter(student=s)
                for d in date_list:
                    a = at.filter(date=d["date"]).order_by("period")

                    total_cnt = a.count()
                    natd_cnt = a.filter(status=1).count()
                    islate = False
                    isearly = False
                    if a.first().status == 1:
                        for i in a:
                            if i.status == 0:
                                islate = True
                                break
                    if a.last().status == 1:
                        for i in a.reverse():
                            if i.status == 0:
                                isearly = True
                                break

                    attendance_count[0] += 1
                    attendance_count[1] += 1 if natd_cnt == total_cnt else 0
                    attendance_count[2] += 1 if islate else 0
                    attendance_count[3] += 1 if isearly else 0

                data = [s.class_num, s.person.name] + attendance_count + [at.exclude(subject=1).count(), at.exclude(subject=1).filter(status=1).count()]
                writer.writerow(data)

        else:
            writer.writerow(["番号", "名前", "授業日数", "欠席日数", "遅刻日数", "早退日数", "授業回数", "欠課数"])
            attendance = Attendance.objects.filter(date__gte=from_date, date__lte=to_date, subject=subject)
            date_list = attendance.values("date").distinct()

            for s in student:
                attendance_count = [0, 0, 0, 0]
                at = attendance.filter(student=s)
                for d in date_list:
                    a = at.filter(date=d["date"]).order_by("period")

                    total_cnt = a.count()
                    natd_cnt = a.filter(status=1).count()
                    islate = False
                    isearly = False
                    if a.first().status == 1:
                        for i in a:
                            if i.status == 0:
                                islate = True
                                break
                    if a.last().status == 1:
                        for i in a.reverse():
                            if i.status == 0:
                                isearly = True
                                break

                    attendance_count[0] += 1
                    attendance_count[1] += 1 if natd_cnt == total_cnt else 0
                    attendance_count[2] += 1 if islate else 0
                    attendance_count[3] += 1 if isearly else 0

                data = [s.class_num, s.person.name] + attendance_count + [at.count(), at.exclude(subject=1).count()]
                writer.writerow(data)

        return response

    else:
        # 404 not found
        return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

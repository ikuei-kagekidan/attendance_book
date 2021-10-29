from django.shortcuts import render


def index(request):
    return render(request, 'attendance_book/index.html')

def teach_in(request):
    return render(request, 'attendance_book/teach_in.html')

def teach_agg(request):
    return render(request, 'attendance_book/teach_agg.html')

def student(request):
    return render(request, 'attendance_book/student.html')

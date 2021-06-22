from django.shortcuts import render


def index(request):
    return render(request, 'attendance_book/index.html')
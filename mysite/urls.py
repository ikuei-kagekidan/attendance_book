from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('attendance_book/', include('attendance_book.urls')),
    path('attendance_book/teacher/input/', include('attendance_book.urls')),
    path('attendance_book/teacher/aggregation/', include('attendance_book.urls')),
    path('attendance_book/student/', include('attendance_book.urls')),
    path('admin/', admin.site.urls),
]


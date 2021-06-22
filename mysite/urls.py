from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('attendance_book/', include('attendance_book.urls')),
    path('admin/', admin.site.urls),
]

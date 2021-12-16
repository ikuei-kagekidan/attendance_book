from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('attendance_book/', include('attendance_book.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/attendance_book/')),
]


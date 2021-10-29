from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teacher/input', views.teach_in, name='teacher/input'),
    path('teacher/aggregation', views.teach_agg, name='teacher/aggregation'),
    path('student', views.student, name='student'),
]

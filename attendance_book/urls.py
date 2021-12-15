from django.urls import path

from . import views

app_name = 'attendance_book'

urlpatterns = [
    path('', views.index, name='index'),
    path('teacher/input/', views.teach_in, name='teacher-input'),
    path('teacher/aggregation/', views.teach_agg, name='teacher-aggregation'),
    path('student/', views.student, name='student'),
    path('teacher/input/post/', views.teach_in_post, name='teacher-input-post'),
    path('teacher/aggregation/post/', views.teach_agg_post, name='teacher-aggregation-post'),
    path('teacher/aggregation/download/', views.teach_agg_download, name='teacher-aggregation-download'),
]

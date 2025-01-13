from django.urls import path, re_path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subjects_list, name='subjects_list'),
    # path('<str:subject_code>/', views.subjects_details, name='subjects_details'),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/edit/',
        views.lessons_edit,
        name='lessons_edit',
    ),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/delete/',
        views.lessons_delete,
        name='lessons_delete',
    ),
    re_path(
        '(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/',
        views.lessons_details,
        name='lessons_details',
    ),
    re_path('(?P<subject_code>[A-Z]{3})/lessons/add/', views.lessons_add, name='lessons_add'),
    re_path('(?P<subject_code>[A-Z]{3})/marks/edit/', views.edit_marks, name='edit_marks'),
    re_path('(?P<subject_code>[A-Z]{3})/marks/', views.subjects_marks, name='subjects_marks'),
    re_path('(?P<subject_code>[A-Z]{3})/', views.subjects_details, name='subjects_details'),
    path('enroll/', views.subjects_enroll, name='subjects_enroll'),
    path('unenroll/', views.subjects_unenroll, name='subjects_unenroll'),
    path('certificate/', views.certificate, name='certificate'),
]

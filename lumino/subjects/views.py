from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import Profile

from .forms import (
    AddLessonForm,
    EditLessonForm,
    EditMarkForm,
    EditMarkFormSetHelper,
    EnrollForm,
    UnenrollForm,
)
from .models import Enrollment, Lesson, Subject
from .tasks import deliver_certificate


@login_required
def subjects_list(request):
    user = request.user
    isteacher = Profile.is_teacher(user)
    if isteacher:
        subjects = Subject.objects.filter(teacher=user)
        return render(request, 'subject_list.html', {'subjects': subjects, 'isteacher': isteacher})
    else:
        subjects = Subject.objects.filter(students=user)
        certificate_on = (
            not Enrollment.objects.filter(student=user, subject__in=subjects)
            .filter(mark__isnull=True)
            .exists()
        )
        return render(
            request,
            'subject_list.html',
            {'isteacher': isteacher, 'certificate_on': certificate_on},
        )


@login_required
def subjects_details(request, subject_code):
    user = request.user
    role = user.profile.role
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        if not check_enrollment(subject, user):
            return HttpResponseForbidden()
    lessons = Lesson.objects.filter(subject=subject)
    isteacher = Profile.is_teacher(user)
    mark = None
    if not isteacher:
        mark = Enrollment.objects.get(subject=subject, student=user).mark
    return render(
        request,
        'subject_details.html',
        {
            'mark': mark,
            'subject': subject,
            'role': role,
            'lessons': lessons,
            'isteacher': isteacher,
        },
    )


@login_required
def lessons_details(request, subject_code, lesson_pk):
    user = request.user
    isteacher = Profile.is_teacher(user)
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        if not check_enrollment(subject, user):
            return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_pk)
    return render(
        request,
        'lesson_details.html',
        {'isteacher': isteacher, 'lesson': lesson, 'subject': subject},
    )


@login_required
def lessons_add(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        user = request.user
        if (form := AddLessonForm(request.POST)).is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject
            lesson.save()
            messages.success(request, 'Lesson was successfully added.')
            return redirect('subjects:subjects_details', subject_code)
    else:
        form = AddLessonForm()
    return render(request, 'lesson_add.html', dict(form=form))


@login_required
def lessons_edit(request, subject_code, lesson_pk):
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_pk)
    if request.method == 'POST':
        if (form := EditLessonForm(request.POST, instance=lesson)).is_valid():
            form.save()
            messages.success(request, 'Changes were successfully saved.')
            return render(request, 'lesson_edit.html', dict(form=form))
    else:
        form = EditLessonForm(instance=lesson)
    return render(request, 'lesson_edit.html', dict(form=form))


@login_required
def lessons_delete(request, subject_code, lesson_pk):
    lesson = Lesson.objects.get(pk=lesson_pk)
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        return HttpResponseForbidden()
    if lesson.subject.teacher == request.user:
        messages.success(request, 'Lesson was successfully deleted.')
        lesson.delete()
    else:
        return HttpResponseForbidden()
    return redirect('subjects:subjects_details', subject_code)


@login_required
def subjects_marks(request, subject_code):
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        return HttpResponseForbidden()
    enrollments = subject.enrollment.all()
    return render(request, 'subject_marks.html', dict(enrollments=enrollments, subject=subject))


@login_required
def edit_marks(request, subject_code: str):
    subject = Subject.objects.get(code=subject_code)
    if subject.teacher != request.user:
        return HttpResponseForbidden()
    MarkFormSet = modelformset_factory(Enrollment, EditMarkForm, extra=0)
    queryset = subject.enrollment.all()
    if request.method == 'POST':
        if (formset := MarkFormSet(queryset=queryset, data=request.POST)).is_valid():
            formset.save()
            messages.success(request, 'Marks were successfully saved.')
            return redirect(reverse('subjects:edit_marks', kwargs={'subject_code': subject_code}))
    else:
        formset = MarkFormSet(queryset=queryset)
    helper = EditMarkFormSetHelper()
    return render(
        request,
        'subjects/marks/edit_marks.html',
        dict(subject=subject, formset=formset, helper=helper),
    )


@login_required
def subjects_enroll(request):
    user = request.user
    if Profile.is_teacher(user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        if (form := EnrollForm(user, request.POST)).is_valid():
            enroll = form.save(user)
            messages.success(request, 'Successfully enrolled in the chosen subjects.')
            return redirect('subjects:subjects_list')
        else:
            messages.error(
                request, 'Hubo un error al intentar inscribirte. Por favor, intenta de nuevo.'
            )
    else:
        form = EnrollForm(user)
    return render(request, 'enroll_subjects.html', dict(form=form))


def check_enrollment(subject, user):
    return subject.enrollment.filter(student=user).exists()


@login_required
def subjects_unenroll(request):
    user = request.user
    if Profile.is_teacher(user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        if (form := UnenrollForm(user, request.POST)).is_valid():
            unenroll = form.save(user)
            messages.success(request, 'Successfully unenrolled from the chosen subjects.')
        else:
            messages.error(
                request, 'Hubo un error al intentar desinscribirte. Por favor, intenta de nuevo.'
            )
        return redirect('subjects:subjects_list')
    else:
        form = UnenrollForm(user)
    return render(request, 'enroll_subjects.html', dict(form=form))


# @login_required
# def certificate(request):
#     user = request.user
#     if Enrollment.objects.filter(mark=None, student=user).count() > 0:
#         return HttpResponseForbidden()
#     if Profile.is_teacher(user):
#         return HttpResponseForbidden()
#     deliver_certificate.delay(request.build_absolute_uri('/'), request.user)

#     return redirect('subjects:subjects_list')


@login_required
def certificate(request):
    if not Profile.is_teacher(request.user):
        if not request.user.enrolled.filter(mark__isnull=True).exists():
            base_url = request.build_absolute_uri('/')
            deliver_certificate.delay(base_url, request)
            msg = f'You will get the grade certificate quite soon at {request.user.email}'

            return render(request, 'msg_certificate.html', dict(msg=msg))
        else:
            messages.error(request, 'You do not have permission to access this resource.')
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

from subjects.models import Subject
from users.models import Profile


def breadcrumbs(request):
    crumbs = []
    if request.resolver_match:
        path_parts = request.path_info.strip('/').split('/')
        current_url = ''

        for part in path_parts:
            current_url += f'/{part}'
            crumbs.append({'title': part.capitalize(), 'url': current_url})

    if crumbs:
        crumbs[-1]['active'] = True

    return {'breadcrumbs': crumbs}


def subjects(request):
    user = request.user

    if user.is_authenticated:
        user = request.user
        isteacher = Profile.is_teacher(user)
        if isteacher:
            subjects = Subject.objects.filter(teacher=user)
        else:
            subjects = Subject.objects.filter(students=user)
        return {'subjects': subjects}
    return {}

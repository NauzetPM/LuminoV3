from django.core.management.base import BaseCommand
from django.db.models import Avg

from subjects.models import Enrollment, Subject


class Command(BaseCommand):
    help = 'Calcula las notas medias de todos los módulos'

    def handle(self, *args, **kwargs):
        subjects = Subject.objects.all()

        for subject in subjects:
            enrollments = Enrollment.objects.filter(subject=subject, mark__isnull=False)

            if enrollments.exists():
                average_mark = enrollments.aggregate(Avg('mark'))['mark__avg']
                self.stdout.write(f'{subject.code}: {average_mark:.2f}')
            else:
                self.stdout.write(f'{subject.code}: No hay notas disponibles')

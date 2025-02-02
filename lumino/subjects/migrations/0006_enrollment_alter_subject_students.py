# Generated by Django 5.1.3 on 2024-12-04 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0005_alter_lesson_title_alter_subject_code_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateField(auto_now_add=True)),
                ('mark', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment_student', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollment', to='subjects.subject')),
            ],
        ),
        migrations.AlterField(
            model_name='subject',
            name='students',
            field=models.ManyToManyField(related_name='students_subjects', through='subjects.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
    ]

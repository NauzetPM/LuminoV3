# Generated by Django 5.1.3 on 2024-12-04 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0006_enrollment_alter_subject_students'),
        ('users', '0003_alter_enrollment_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Enrollment',
        ),
    ]
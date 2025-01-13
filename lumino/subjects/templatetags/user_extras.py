# user_extras.py
from django import template

register = template.Library()


@register.filter
def fullname(student):
    return f'{student.first_name} {student.last_name}'

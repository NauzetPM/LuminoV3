import datetime
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from weasyprint import HTML


@job
def deliver_certificate(base_url, request):
    rendered = render_to_string(
        'subjects/certificate/certificate.html',
        {
            'student': request.user,
            'today': datetime.date.today(),
            'request': request,
        },
    )

    output_path = os.path.join(
        settings.CERTIFICATES_DIR, f'{request.user.username}_grade_certificate.pdf'
    )
    os.makedirs(settings.CERTIFICATES_DIR, exist_ok=True)
    HTML(string=rendered, base_url=base_url).write_pdf(output_path)

    email_body = render_to_string('subjects/certificate/email.md', {'student': request.user})

    email = EmailMessage(
        subject='Grade Certificate',
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email],
    )
    email.content_subtype = 'html'
    email.attach_file(output_path)
    email.send()

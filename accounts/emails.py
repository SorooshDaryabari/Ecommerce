from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_email_activation_code(name, email, activate_code_url):
    context = {
        "name": name,
        "activate_code_url": activate_code_url
    }

    email_subject = "َActivate your account"
    email_body = render_to_string("activate_email", context=context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email, ],
    )
    return email.send(fail_silently=False)

from django.core.mail import send_mail as django_send_mail
from port import settings

def send_feedback_mail(uniemail):
    mail_subject = "Feedback mail from Naga Arjun"
    message = "Thank you for providing feedback and instructions to us."
    to_email = uniemail

    django_send_mail(  # Use Django's send_mail function explicitly
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
    )
    return "Sent email successfully"

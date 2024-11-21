from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail

@receiver(post_save, sender=Quotation)
def notify_customer(sender, instance, created, **kwargs):
    if created:
        customer_email = instance.project.customer.user.email
        send_mail(
            subject="New Quotation Available",
            message=f"A new Quotation by '{instance.service_provider}' for your project '{instance.project.name}' (Stage: '{instance.stage}' has been provided)",
            from_email="noreply@ardy-app.com",
            recipient_list=[customer_email],
            )
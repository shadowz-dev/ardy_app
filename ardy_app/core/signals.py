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
            message=f"A new Quotation by '{instance.service_provider}' for project '{instance.project.title}' (Stage: '{instance.stage}' has been provided)",
            from_email="noreply@ardy-app.com",
            recipient_list=[customer_email],
            )
        

@receiver(post_save, sender=Drawing)
def notify_customer_on_drawing(sender, instance, created, **kwargs):
    if created:
        customer_email = instance.project.customer.user.email
        send_mail(
            subject="New Drawing Uploaded",
            message=f"A new Drawing by '{instance.service_provider}' for project '{instance.project.title}' has been uploaded)",
            from_email="noreply@ardy-app.com",
            recipient_list=[customer_email],
            )
        
@receiver(post_save, sender=Revision)
def notify_service_provider_on_revision(sender, instance, created, **kwargs):
    if created:
        service_provider_email = instance.drawing.service_provider.email
        send_mail(
            subject="New Revision Requested",
            message=f"A new Revision Requested for drawing '{instance.drawing.id}' by customer",
            from_email="noreply@ardy-app.com",
            recipient_list=[service_provider_email],
        )
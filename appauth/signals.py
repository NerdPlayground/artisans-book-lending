from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # get the recipient name or usernamae
    recipient="{} {}".format(reset_password_token.user.first_name,reset_password_token.user.last_name)
    if recipient=="": recipient=reset_password_token.user.username

    # create the password reset message
    reset_link=instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))
    reset_token=reset_password_token.key
    instructions=f"Open the link to reset your password:\nLink: {reset_link}\nAuthentication Token: {reset_token}"
    email_plaintext_message=f"{instructions}\n NOTE: The Authentication Token is valid for 24 hours"

    send_mail(
        subject=f"Password Reset for {recipient}",
        message=email_plaintext_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reset_password_token.user.email],
        fail_silently=False,
    )
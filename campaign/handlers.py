from urllib.parse import urlparse

from corsheaders.signals import check_request_enabled
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from mailqueue.models import MailerMessage

from campaign.models import Campaign, ReferralInvite, ReferralSignup


def cors_allow_mysites(sender, request, **kwargs):
    origin = request.META.get('HTTP_ORIGIN')
    if origin:
        return Campaign.objects.filter(
            signup_success_host=urlparse(origin).netloc).exists()

    return True  # FIXME: Need to decide what to do with hidden origins.


check_request_enabled.connect(cors_allow_mysites)


@receiver(pre_save, sender=Campaign)
def save_host(sender, instance, **kwargs):
    """ Update success host. """
    if instance.signup_success_url:
        instance.signup_success_host = urlparse(instance.signup_success_url).netloc


@receiver(post_save, sender=ReferralInvite)
def notify_referral_invite(sender, instance, created, **kwargs):
    if created:
        new_message = MailerMessage()
        new_message.subject = instance.subject
        new_message.to_address = instance.email
        new_message.bcc_address = 'buzzlyapp+invites@gmail.com'
        new_message.from_address = instance.referral.referrer
        new_message.reply_to = instance.referral.referrer
        new_message.content = instance.message
        new_message.html_content = instance.html_message
        new_message.app = 'Campaign'
        new_message.save()


@receiver(post_save, sender=ReferralSignup)
def notify_referral_signup(sender, instance, created, **kwargs):
    if created:
        new_message = MailerMessage()
        new_message.subject = 'A new signup!'
        new_message.to_address = instance.referral.campaign.user.email
        new_message.bcc_address = 'buzzlyapp+signups@gmail.com'
        new_message.from_address = 'buzzlyapp@gmail.com'
        new_message.reply_to = 'buzzlyapp@gmail.com'
        new_message.content = 'View the new signup at: https://www.buzzlyapp.com/dashboard/'
        new_message.app = 'Campaign'
        new_message.save()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        context = {}
        new_message = MailerMessage()
        new_message.subject = 'Buzzly - Welcome!'
        new_message.to_address = instance.email
        new_message.bcc_address = 'buzzlyapp+signups@gmail.com'
        new_message.from_address = 'buzzlyapp@gmail.com'
        new_message.reply_to = 'buzzlyapp@gmail.com'
        new_message.html_content = render_to_string('email/welcome.html', context)
        new_message.app = 'Campaign'
        new_message.save()

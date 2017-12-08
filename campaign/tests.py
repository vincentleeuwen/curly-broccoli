# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from mailqueue.models import MailerMessage

from campaign.models import Campaign, Referral, ReferralInvite, ReferralSignup


class CampaignTest(TestCase):

    def setUp(self):
        self.company = 'Awesome company'
        self.signup_url = 'https://www.wineclub.nl/signup/'
        self.email = 'vincentleeuwen@gmail.com'
        self.password = 'password'
        self.new_user = User.objects.create_user(
            username='John',
            email='johnlennon@gmail.com',
            password='foobar',
        )
        self.campaigns = Campaign.objects.count()
        self.campaign = Campaign.objects.create(
            user=self.new_user,
            company=self.company,
            product='Test product',
            reward='Test reward',
            signup_url='https://www.wineclub.nl/signup/'
        )
        self.referral = Referral.objects.create(
            campaign=self.campaign,
            referrer=self.email,
            name='Vincent'
        )

    def test_user_welcome_mail_generated(self):
        self.assertEqual(MailerMessage.objects.last().subject, 'Buzzly - Welcome!')
        self.assertEqual(MailerMessage.objects.last().to_address, 'johnlennon@gmail.com')

    def test_create_campaign_signal(self):
        self.assertEqual(Campaign.objects.count() - self.campaigns, 1)
        self.campaign.signup_success_url = 'https://www.wineclub.nl/order/success/'
        self.campaign.save()
        self.assertEqual(self.campaign.signup_success_host, 'www.wineclub.nl')

    def test_create_referral_invite_signal(self):
        email = 'foo@barrr.co'
        mm = MailerMessage.objects.count()
        invite = ReferralInvite.objects.create(
            referral=self.referral,
            email=email
        )
        self.assertEqual(MailerMessage.objects.count() - mm, 1)
        self.assertEqual(
            MailerMessage.objects.last().subject, 'Vincent has invited you to try Awesome company')
        self.assertEqual(
            MailerMessage.objects.last().content,
            'Vincent has invited you to try {0}. Sign up via the link below: \n {1}'.format(
                self.company,
                invite.referral_url,
            )
        )
        self.assertEqual(MailerMessage.objects.last().from_address, self.referral.referrer)
        self.assertEqual(MailerMessage.objects.last().to_address, email)
        invite.save()
        # make sure signal only triggers on create
        self.assertEqual(MailerMessage.objects.count() - mm, 1)

    def test_create_referral_invite_success(self):
        email = 'foo@barrr.co'
        mm = MailerMessage.objects.count()
        ReferralSignup.objects.create(
            referral=self.referral,
            email=email
        )
        self.assertEqual(MailerMessage.objects.count() - mm, 1)
        self.assertEqual(MailerMessage.objects.last().subject, 'A new signup!')
        self.assertEqual(MailerMessage.objects.last().to_address, self.new_user.email)

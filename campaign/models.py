# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from model_utils.models import TimeStampedModel
# from hashid_field import HashidAutoField


class Campaign(TimeStampedModel):
    user = models.ForeignKey(User)
    company = models.CharField(max_length=140)
    product = models.CharField(max_length=256)
    reward = models.TextField()
    top_bar_color = models.CharField(max_length=7, default='#f8f8f8')
    logo = models.ImageField(upload_to='logos/', blank=True)
    signup_url = models.URLField(blank=True, help_text='Url where referrals are led to')
    signup_success_url = models.URLField(
        blank=True,
        help_text='Url where user ends up after signing up (used for conversion)'
    )
    signup_success_host = models.CharField(max_length=200, blank=True)

    @property
    def referral_link(self):
        return 'https://www.buzzlyapp.com/campaign/{0}'.format(self.pk)

    @property
    def is_live(self):
        return self.product and self.reward and self.signup_url and self.signup_success_url


class Referral(TimeStampedModel):
    campaign = models.ForeignKey(Campaign)
    referrer = models.EmailField()
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return '{0}'.format(self.referrer)


class ReferralInvite(TimeStampedModel):
    referral = models.ForeignKey(Referral)
    email = models.EmailField()

    @property
    def referral_url(self):
        return '{0}?buzzlyref={1}&buzzlyemail={2}'.format(
            self.referral.campaign.signup_url,
            self.referral.pk,
            self.email
        )

    @property
    def subject(self):
        if self.referral.name:
            return '{0} has invited you to try {1}'.format(
                self.referral.name,
                self.referral.campaign.company
            )
        return "You've been invited to try {0}.".format(self.referral.campaign.company)

    @property
    def message(self):
        if self.referral.name:
            return '{0} has invited you to try {1}. Sign up via the link below: \n {2}'.format(
                self.referral.name,
                self.referral.campaign.company,
                self.referral_url,
            )

        return "You've been invited to try {0}. Sign up via the link below: \n {1}".format(
            self.referral.campaign.company,
            self.referral_url,
        )

    @property
    def html_message(self):
        if self.referral.name:
            return '<p>{0} has invited you to try {1}. Learn more via the link below:</p><p><a href="{2}">{2}</a></p>'.format(
                self.referral.name,
                self.referral.campaign.company,
                self.referral_url,
            )

        return "<p>You've been invited to try {0}. Learn more via the link below:</p><p><a href='{1}'>{1}</a></p>".format(
            self.referral.campaign.company,
            self.referral_url,
        )


class ReferralSignup(TimeStampedModel):
    referral = models.ForeignKey(Referral)
    email = models.EmailField(blank=True)
    followed_up = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

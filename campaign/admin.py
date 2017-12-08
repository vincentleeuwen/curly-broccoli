# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from campaign.models import Campaign, Referral, ReferralInvite, ReferralSignup


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'product', 'reward', 'created', 'modified']


class ReferralAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'referrer', 'name', 'created', 'modified']


class ReferralInviteAdmin(admin.ModelAdmin):
    list_display = ['referral', 'email', 'created', 'modified']


class ReferralSignupAdmin(admin.ModelAdmin):
    list_display = ['id', 'referral', 'email', 'followed_up', 'created', 'modified']


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Referral, ReferralAdmin)
admin.site.register(ReferralInvite, ReferralInviteAdmin)
admin.site.register(ReferralSignup, ReferralSignupAdmin)

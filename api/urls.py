from django.conf.urls import url
from rest_framework.authtoken import views as api_views

from api import views


urlpatterns = [
    url(r'^create-campaign/$', views.CreateCampaignView.as_view(), name='create_campaign'),
    url(r'^campaigndata/(?P<pk>[0-9]+)/$', views.GetCampaignView.as_view(), name='get_campaign'),
    url(r'^campaign/(?P<pk>[0-9]+)/$', views.UpdateCampaignView.as_view(), name='update_campaign'),
    url(
        r'^campaign/logo/(?P<pk>[0-9]+)/$',
        views.UpdateCampaignLogoView.as_view(), name='update_campaign_logo'),
    url(r'^campaigns/$', views.ListCampaignsView.as_view(), name='list_campaigns'),
    url(r'^create-user/$', views.CreateUserView.as_view(), name='create_user'),
    url(r'^create-referral/$', views.CreateReferralView.as_view(), name='create_referral',),
    url(
        r'^create-referral-invite/$',
        views.CreateReferralInviteView.as_view(), name='create_referral_invite'),
    url(
        r'^create-referral-signup/$',
        views.CreateReferralSignupView.as_view(), name='create_referral_signup'),
    url(
        r'^update-referral-signup/(?P<pk>[0-9]+)/$',
        views.UpdateReferralSignupView.as_view(), name='update_referral_signup'),
    url(r'^referral-signups/$', views.ReferralSignupListView.as_view(), name='list_referrals'),
    url(r'^check-email/', views.CheckUserView.as_view(), name='check_email'),
    url(r'^create-subscription/', views.CreateSubscriptionView.as_view(), name='create_subscription'),
    url(r'^api-token-auth/', api_views.obtain_auth_token),
]

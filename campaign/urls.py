from django.conf.urls import url

from campaign import views


urlpatterns = [
    url(r'^(?P<pk>[-\w]+).js$', views.CampaignScriptView.as_view(), name='campaign'),
    url(r'^(?P<pk>[-\w]+).min.js$', views.CampaignScriptMinifiedView.as_view(), name='campaign_minified'),
]

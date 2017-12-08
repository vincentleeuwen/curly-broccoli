# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from campaign.models import Campaign


class CampaignScriptView(DetailView):
    template_name = 'script.js'
    model = Campaign

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(
            context, content_type='application/x-javascript')


class CampaignScriptMinifiedView(DetailView):
    template_name = 'script.min.js'
    model = Campaign

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(
            context, content_type='application/x-javascript')

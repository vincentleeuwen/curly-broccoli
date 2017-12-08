# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CampaignConfig(AppConfig):
    name = 'campaign'

    def ready(self):
        from . import handlers

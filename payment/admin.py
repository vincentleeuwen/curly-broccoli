from django.contrib import admin

from payment.models import StripeSubscription


class StripeSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'sub_id', 'created']

admin.site.register(StripeSubscription, StripeSubscriptionAdmin)

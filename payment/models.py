from django.db import models
from model_utils.models import TimeStampedModel


class StripeCustomer(TimeStampedModel):
    email = models.EmailField()
    stripe_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return '{0}'.format(self.email)


class StripeSubscription(TimeStampedModel):
    customer = models.ForeignKey(StripeCustomer)
    sub_id = models.CharField(max_length=255, unique=True)

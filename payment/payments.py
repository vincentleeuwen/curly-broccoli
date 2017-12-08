import logging

from django.conf import settings
import stripe

from payment.models import StripeCustomer, StripeSubscription


class StripePayment:
    logger = logging.getLogger(__name__)

    def create_new_subscription(self, email, source):
        customer = self.create_new_customer(email, source).get('id')
        if customer:
            stripe_customer = StripeCustomer.objects.create(
                email=email,
                stripe_id=customer
            )
            subscription = stripe.Subscription.create(
                customer=customer,
                items=[
                    {
                        'plan': 'basic',  # NOTE: For now, there's only one plan.
                    },
                ],
            )
            if subscription.get('id'):
                StripeSubscription.objects.create(
                    customer=stripe_customer,
                    sub_id=subscription.get('id')
                )
        return subscription

    def create_new_customer(self, email, source):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            resp = stripe.Customer.create(
                description='Buzzly customer {0}'.format(email),
                source=source,
                email=email
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']

            self.logger.debug("Status is: %s" % e.http_status)
            self.logger.debug("Type is: %s" % err['type'])
            self.logger.debug("Code is: %s" % err['code'])
            # param is '' in this case
            self.logger.debug("Param is: %s" % err['param'])
            self.logger.debug("Message is: %s" % err['message'])
            self.logger.error(
                'Stripe card error processing {0}. Message {1}'.format(
                    email, err['message']))
            self.logger.error(
                'Je credit card is helaas geweigerd. Kloppen alle velden wel?')
            raise e
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            self.logger.error(
                'Stripe rate limit error processing {0}. Error: {1}'.format(
                    email, e))
            raise e
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            self.logger.error(
                'Stripe invalid request error processing {0}. Error: {1}'.format(
                    email, e))
            raise e
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            self.logger.error('Stripe authentication error processing {0}. Error: {1}'.format(
                email, e))
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            self.logger.error('Stripe API error processing {0}. Error: {1}'.format(
                email, e))
        except stripe.error.StripeError as e:
            self.logger.error('Stripe error processing {0}. Error: {1}'.format(
                email, e))
            raise e
            # Display a very generic error to the user, and maybe send
            # yourself an email
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            self.logger.error('Stripe error processing {0}. Error: {1}'.format(email, e))
            raise e
        else:
            return resp

from django.test import TestCase

from payment.payments import StripePayment
from payment.models import StripeCustomer, StripeSubscription


class PaymentTest(TestCase):

    def setUp(self):
        self.source = dict(
            exp_month='12',
            exp_year='2022',
            number='4242424242424242',
            cvc='999',
            name='name_on_card',
        )
        self.source['object'] = 'card'

    def test_create_customer(self):
        resp = StripePayment().create_new_customer(
            source=self.source,
            email='testuser@buzzlyapp.com',
        )
        self.assertIsNotNone(resp.get('sources'))
        self.assertIsNotNone(resp.get('id'))
        self.assertEqual(resp['id'][0:3], 'cus')
        self.assertFalse(resp['livemode'])

    def test_create_subscription(self):
        customers = StripeCustomer.objects.count()
        subs = StripeSubscription.objects.count()
        resp = StripePayment().create_new_subscription(
            email='testuser@buzzlyapp.com',
            source=self.source
        )
        self.assertIsNotNone(resp.get('id'))
        self.assertIsNotNone(resp.get('billing'))
        self.assertEqual(resp['id'][0:3], 'sub')
        self.assertEqual(resp['customer'][0:3], 'cus')
        self.assertEqual(resp['plan']['name'], 'basic')
        self.assertEqual(resp['plan']['trial_period_days'], 14)
        self.assertFalse(resp['livemode'])
        self.assertEqual(StripeCustomer.objects.count() - customers, 1)
        self.assertEqual(StripeSubscription.objects.count() - subs, 1)

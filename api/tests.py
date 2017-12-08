import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from campaign.models import Campaign, Referral, ReferralInvite, ReferralSignup


class ApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = 'vincentleeuwen@gmail.com'
        self.password = 'password'
        self.users = User.objects.count()
        self.client.post(
            reverse('api:create_user'),
            dict(
                username=self.email,
                email=self.email,
                password=self.password
            )
        )
        self.tokens = Token.objects.count()
        self.new_user = User.objects.order_by('-pk').first()
        url = '/api/api-token-auth/'
        data = dict(
            username=self.new_user.username,
            password=self.password,
        )
        response = self.client.post(url, data=data)
        self.token_json_data = json.loads(response.content)

    def test_user_creation_success(self):
        self.assertEqual(User.objects.count() - self.users, 1)
        new_user = User.objects.order_by('-pk').first()
        self.assertEqual(new_user.username, self.email)
        self.assertEqual(new_user.email, self.email)

    def test_obtain_token(self):
        self.assertEqual(User.objects.count() - self.users, 1)

        self.assertEqual(self.new_user.username, self.email)
        self.assertEqual(self.new_user.email, self.email)
        # make sure we get a token response and test name
        self.assertTrue(self.token_json_data.get('token'), False)
        self.assertEqual(Token.objects.count() - self.tokens, 1)
        self.assertEqual(Token.objects.order_by('-pk').first().user, self.new_user)

    def test_create_campaign(self):
        campaigns = Campaign.objects.count()
        self.assertTrue(self.client.login(
            username=self.email, password=self.password))
        data = dict(
            company='Test company',
            product='Test product',
            reward='First reward',
        )
        response = json.loads(self.client.post(reverse('api:create_campaign'), data).content)

        self.assertEqual(data['product'], response['product'])
        self.assertEqual(data['reward'], response['reward'])
        self.assertEqual(Campaign.objects.last().product, data['product'])
        self.assertEqual(Campaign.objects.last().reward, data['reward'])
        self.assertEqual(Campaign.objects.last().user, self.new_user)
        self.assertEqual(Campaign.objects.count() - campaigns, 1)

    def test_update_campaign(self):
        campaigns = Campaign.objects.count()
        self.assertTrue(self.client.login(
            username=self.email, password=self.password))
        data = dict(
            company='Test company',
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com'
        )
        response = json.loads(self.client.post(reverse('api:create_campaign'), data).content)
        self.assertEqual(data['product'], response['product'])
        self.assertEqual(data['reward'], response['reward'])
        self.assertEqual(Campaign.objects.last().product, data['product'])
        self.assertEqual(Campaign.objects.last().reward, data['reward'])
        self.assertEqual(Campaign.objects.last().user, self.new_user)
        self.assertEqual(Campaign.objects.count() - campaigns, 1)
        new_data = dict(
            company='Test company',
            product='Test product 2',
            reward='Second reward',
        )
        response = json.loads(
            self.client.put('/api/campaign/{0}/'.format(response['id']), new_data).content)
        self.assertEqual(Campaign.objects.last().product, new_data['product'])
        self.assertNotEqual(Campaign.objects.last().product, data['product'])
        self.assertEqual(Campaign.objects.last().reward, new_data['reward'])
        self.assertNotEqual(Campaign.objects.last().reward, data['reward'])

    def test_list_campaigns(self):
        campaigns = Campaign.objects.count()
        self.assertTrue(self.client.login(
            username=self.email, password=self.password))
        data = dict(
            company='Test company',
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com'
        )
        response = json.loads(self.client.post(reverse('api:create_campaign'), data).content)
        self.assertEqual(data['product'], response['product'])
        self.assertEqual(data['reward'], response['reward'])
        self.assertEqual(Campaign.objects.last().product, data['product'])
        self.assertEqual(Campaign.objects.last().reward, data['reward'])
        self.assertEqual(Campaign.objects.last().user, self.new_user)
        self.assertEqual(Campaign.objects.count() - campaigns, 1)
        response = json.loads(self.client.get(reverse('api:list_campaigns')).content)
        self.assertEqual(len(response), Campaign.objects.filter(user=self.new_user).count())

    def test_referral_creation(self):
        referrals = Referral.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        data = dict(
            campaign=campaign.id,
            referrer=referrer,
        )
        response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
        self.assertIsNotNone(response)
        self.assertEqual(response['campaign'], campaign.id)
        self.assertEqual(response['referrer'], referrer)
        self.assertEqual(Referral.objects.count() - referrals, 1)
        self.assertEqual(Referral.objects.last().campaign, campaign)
        self.assertEqual(Referral.objects.last().referrer, referrer)

    def test_duplicate_referral_creation(self):
        referrals = Referral.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        data = dict(
            campaign=campaign.id,
            referrer=referrer,
        )
        response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
        self.assertIsNotNone(response)
        self.assertEqual(response['campaign'], campaign.id)
        self.assertEqual(response['referrer'], referrer)
        self.assertEqual(Referral.objects.count() - referrals, 1)
        self.assertEqual(Referral.objects.last().campaign, campaign)
        self.assertEqual(Referral.objects.last().referrer, referrer)
        response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
        self.assertIsNotNone(response)
        self.assertEqual(response['campaign'], campaign.id)
        self.assertEqual(response['referrer'], referrer)
        self.assertEqual(Referral.objects.count() - referrals, 1)

    def test_duplicate_campaign_same_referrer(self):
        referrals = Referral.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        data = dict(
            campaign=campaign.id,
            referrer=referrer,
        )
        response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
        self.assertIsNotNone(response)
        self.assertEqual(response['campaign'], campaign.id)
        self.assertEqual(response['referrer'], referrer)
        self.assertEqual(Referral.objects.count() - referrals, 1)
        self.assertEqual(Referral.objects.last().campaign, campaign)
        self.assertEqual(Referral.objects.last().referrer, referrer)
        new_campaign = Campaign.objects.create(
            user=self.new_user,
            product='Another Test product',
            reward='Another reward',
            signup_url='https://anothertest.buzzlyapp.com',
        )
        data = dict(
            campaign=new_campaign.id,
            referrer=referrer,
        )
        response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
        self.assertIsNotNone(response)
        self.assertEqual(response['campaign'], new_campaign.id)
        self.assertEqual(response['referrer'], referrer)
        self.assertEqual(Referral.objects.count() - referrals, 2)
        self.assertEqual(response['campaign'], new_campaign.id)
        self.assertEqual(response['referrer'], referrer)

        def test_same_campaign_different_referrer(self):
            referrals = Referral.objects.count()
            campaign = Campaign.objects.create(
                user=self.new_user,
                product='Test product',
                reward='First reward',
                signup_url='https://test.buzzlyapp.com',
            )
            referrer = 'testuser@buzzlyapp.com'
            data = dict(
                campaign=campaign.id,
                referrer=referrer,
            )
            response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
            self.assertIsNotNone(response)
            self.assertEqual(response['campaign'], campaign.id)
            self.assertEqual(response['referrer'], referrer)
            self.assertEqual(Referral.objects.count() - referrals, 1)
            self.assertEqual(Referral.objects.last().campaign, campaign)
            self.assertEqual(Referral.objects.last().referrer, referrer)
            first_item = Referral.objects.last()
            data = dict(
                campaign=campaign.id,
                referrer='another_cool_referrer@gmail.com',
            )
            response = json.loads(self.client.post(reverse('api:create_referral'), data).content)
            self.assertIsNotNone(response)
            self.assertEqual(response['campaign'], campaign.id)
            self.assertEqual(response['referrer'], referrer)
            self.assertEqual(Referral.objects.count() - referrals, 2)
            self.assertEqual(response['campaign'], campaign.id)
            self.assertEqual(response['referrer'], referrer)
            self.assertNotEqual(first_item, Referral.objects.last())

    def test_create_referral_invite(self):
        referral_invites = ReferralInvite.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)

    def test_create_referral_invite_no_duplicates(self):
        referral_invites = ReferralInvite.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 1)

    def test_create_referral_invite_multiple_emails(self):
        referral_invites = ReferralInvite.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)
        invitee = 'another_invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 2)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)

    def test_create_referral_invite_multiple_referrals(self):
        referral_invites = ReferralInvite.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Another Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)
        second_referral = Referral.objects.create(
            campaign=campaign,
            referrer='another_testuser@buzzlyapp.com',
        )
        data = dict(
            referral=second_referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_invite'), data).content)
        self.assertEqual(ReferralInvite.objects.count() - referral_invites, 2)
        self.assertEqual(response['referral'], second_referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralInvite.objects.last().referral, second_referral)
        self.assertEqual(ReferralInvite.objects.last().email, invitee)

    def test_create_referral_signup(self):
        referral_signups = ReferralSignup.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Another Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_signup'), data).content)
        self.assertEqual(ReferralSignup.objects.count() - referral_signups, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralSignup.objects.last().referral, referral)
        self.assertEqual(ReferralSignup.objects.last().email, invitee)
        self.assertFalse(ReferralSignup.objects.last().followed_up)
        second_referral = Referral.objects.create(
            campaign=campaign,
            referrer='another_testuser@buzzlyapp.com',
        )
        data = dict(
            referral=second_referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_signup'), data).content)
        self.assertEqual(ReferralSignup.objects.count() - referral_signups, 2)
        self.assertEqual(response['referral'], second_referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertNotEqual(ReferralSignup.objects.last().referral, second_referral)
        self.assertEqual(ReferralSignup.objects.last().email, invitee)

    def test_update_referral_signup(self):
        referral_signups = ReferralSignup.objects.count()
        campaign = Campaign.objects.create(
            user=self.new_user,
            product='Another Test product',
            reward='First reward',
            signup_url='https://test.buzzlyapp.com',
        )
        referrer = 'testuser@buzzlyapp.com'
        referral = Referral.objects.create(
            campaign=campaign,
            referrer=referrer,
        )
        invitee = 'invited@friend.com'
        data = dict(
            referral=referral.id,
            email=invitee,
        )
        response = json.loads(self.client.post(reverse('api:create_referral_signup'), data).content)
        self.assertEqual(ReferralSignup.objects.count() - referral_signups, 1)
        self.assertEqual(response['referral'], referral.id)
        self.assertEqual(response['email'], invitee)
        self.assertEqual(ReferralSignup.objects.last().referral, referral)
        self.assertEqual(ReferralSignup.objects.last().email, invitee)
        self.assertFalse(ReferralSignup.objects.last().followed_up)
        data = dict(
            followed_up=True,
        )
        self.assertTrue(self.client.login(
            username=self.email, password=self.password))
        response = json.loads(
            self.client.put(
                reverse(
                    'api:update_referral_signup',
                        kwargs={'pk': ReferralSignup.objects.last().id}), data).content)
        self.assertEqual(ReferralSignup.objects.count() - referral_signups, 1)
        self.assertTrue(ReferralSignup.objects.last().followed_up)

    def test_user_check_not_present(self):
        resp = json.loads(self.client.post(
            reverse('api:check_email'), dict(email='foo@barrrr.co')).content)
        self.assertFalse(resp)

    def test_user_check_present(self):
        resp = json.loads(self.client.post(
            reverse('api:check_email'), dict(email=self.email)).content)
        self.assertTrue(resp)

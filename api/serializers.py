from rest_framework import serializers
from django.contrib.auth.models import User
# from app.utils import hash_email
from campaign.models import Campaign, Referral, ReferralInvite, ReferralSignup


class CampaignSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=1)  # we override this based on headers
    is_live = serializers.BooleanField(read_only=True)

    class Meta:
        model = Campaign
        fields = (
            'id',
            'user',
            'product',
            'reward',
            'top_bar_color',
            'logo',
            'signup_url',
            'signup_success_url',
            'company',
            'is_live',
        )
        read_only_fields = ('id', 'logo')


class CampaignLogoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=1)  # we override this based on headers

    class Meta:
        model = Campaign
        fields = (
            'id',
            'user',
            'logo',
        )
        read_only_fields = ('id',)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
        fields = ('id', 'campaign', 'referrer', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        obj, created = Referral.objects.get_or_create(**validated_data)
        return obj


class ReferralInviteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralInvite
        fields = ('referral', 'email')

    def create(self, validated_data):
        obj, created = ReferralInvite.objects.get_or_create(**validated_data)
        return obj


class ReferralSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferralSignup
        fields = ('referral', 'email')


class ReferralSignupListSerializer(serializers.ModelSerializer):
    referral = ReferralSerializer()

    class Meta:
        model = ReferralSignup
        fields = ('id', 'referral', 'email', 'followed_up', 'created', 'modified')


class UpdateReferralSignupSerializer(serializers.ModelSerializer):
    '''
    For now we only allow `followed_up` to be updated,
    so we need a serperate serializer.
    '''

    class Meta:
        model = ReferralSignup
        fields = ('id', 'followed_up')


class CreateSubscriptionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=255)


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

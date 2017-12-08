from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, \
    ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api import serializers

from campaign.models import Campaign, ReferralSignup
from payment.payments import StripePayment
from campaign.models import Campaign


class CreateCampaignView(CreateAPIView):
    serializer_class = serializers.CampaignSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCampaignsView(ListAPIView):
    serializer_class = serializers.CampaignSerializer

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetCampaignView(RetrieveAPIView):
    serializer_class = serializers.CampaignSerializer
    queryset = Campaign.objects.all()
    permission_classes = (permissions.AllowAny,)


class UpdateCampaignView(RetrieveUpdateAPIView):
    serializer_class = serializers.CampaignSerializer

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UpdateCampaignLogoView(RetrieveUpdateAPIView):
    serializer_class = serializers.CampaignLogoSerializer

    def get_queryset(self):
        return Campaign.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    permission_classes = (permissions.AllowAny,)


class CreateReferralView(CreateAPIView):
    serializer_class = serializers.ReferralSerializer
    permission_classes = (permissions.AllowAny,)


class CreateReferralInviteView(CreateAPIView):
    serializer_class = serializers.ReferralInviteSerializer
    permission_classes = (permissions.AllowAny,)


class CreateReferralSignupView(CreateAPIView):
    serializer_class = serializers.ReferralSignupSerializer
    permission_classes = (permissions.AllowAny,)


class ReferralSignupListView(ListAPIView):
    serializer_class = serializers.ReferralSignupListSerializer

    def get_queryset(self):
        return ReferralSignup.objects.filter(referral__campaign__user=self.request.user)


class UpdateReferralSignupView(UpdateAPIView):
    serializer_class = serializers.UpdateReferralSignupSerializer

    def get_queryset(self):
        return ReferralSignup.objects.filter(referral__campaign__user=self.request.user)


class CreateSubscriptionView(APIView):
    serializer_class = serializers.CreateSubscriptionSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sub = StripePayment().create_new_subscription(
                email=serializer.validated_data['email'],
                source=serializer.validated_data['token']
            )
            if sub.get('id'):
                return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


class CheckUserView(APIView):
    serializer_class = serializers.UserEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(User.objects.filter(
                email=serializer.validated_data['email']).count() > 0)
        return Response(status.HTTP_400_BAD_REQUEST)

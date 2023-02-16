from constance import config
from django.core.mail import send_mail
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from digital_agenda.apps.core.serializers import FeedbackSerializer

EMAIL_TEMPLATE = """
New feedback received:

 - URL: %(url)s
 - Email Address: %(email)s

Feedback message:

%(message)s
"""


class FeedbackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    hide_not_auth = True
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        send_mail(
            "[Digital Agenda Data] New feedback received",
            EMAIL_TEMPLATE % serializer.validated_data,
            None,
            [config.FEEDBACK_EMAIL],
        )

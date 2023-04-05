from constance import config
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from digital_agenda.apps.core.serializers import FeedbackSerializer
from digital_agenda.apps.core.jobs import send_mail_job

EMAIL_TEMPLATE = """
New feedback received:

 - URL: %(url)s
 - Email Address: %(email)s

Feedback message:

%(message)s
"""

EMAIL_TEMPLATE_AUTHOR = """
Your message has been recorded, we'll get back to you soon.

Feedback message:

%(message)s
"""


class FeedbackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        send_mail_job.delay(
            "[Digital Agenda Data] New feedback received",
            EMAIL_TEMPLATE % serializer.validated_data,
            None,
            config.FEEDBACK_EMAIL.split(","),
        )
        if serializer.validated_data["email"]:
            send_mail_job.delay(
                "[Digital Agenda Data] Your feedback has been received",
                EMAIL_TEMPLATE_AUTHOR % serializer.validated_data,
                None,
                [serializer.validated_data["email"]],
            )

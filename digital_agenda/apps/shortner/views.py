from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from digital_agenda.apps.shortner.models import ShortURL
from digital_agenda.apps.shortner.serializers import ShortURLSerializer


class ChartRedirectView(TemplateView):
    template_name = "chart_redirect.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = get_object_or_404(ShortURL, pk=kwargs["id"])
        context["obj"] = obj
        if obj.chart.chart_group.image:
            context["image"] = self.request.build_absolute_uri(
                obj.chart.chart_group.image.url
            )
        return context


class CreateShortURLViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = ShortURL
    serializer_class = ShortURLSerializer
    permission_classes = (AllowAny,)

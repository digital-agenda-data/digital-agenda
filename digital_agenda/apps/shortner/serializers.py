from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework.reverse import reverse

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.shortner.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    chart = serializers.SlugRelatedField(
        slug_field="code",
        many=False,
        read_only=False,
        queryset=Chart.objects.filter(is_draft=False),
    )
    short_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShortURL
        fields = ["id", "chart", "query_arguments", "short_url"]

    def get_short_url(self, obj):
        return reverse(
            "chart_redirect",
            kwargs={"id": obj.id},
            request=self.context["request"],
        )

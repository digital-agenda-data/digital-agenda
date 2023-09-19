from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueTogetherValidator

from digital_agenda.apps.charts.models import Chart
from digital_agenda.apps.shortner.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    chart = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field="charts.Chart.id"),
        many=False,
        read_only=False,
        queryset=Chart.objects.all(),
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

    def get_validators(self):
        result = []
        for validator in super().get_validators():
            if isinstance(validator, UniqueTogetherValidator) and validator.fields == (
                "chart",
                "query_arguments",
            ):
                continue
            result.append(validator)

        return result

    def create(self, validated_data):
        try:
            # First check if there is a unique short URL already generated for this
            # chart. To avoid errors if users create the same short url multiple times.
            return ShortURL.objects.get(
                chart=validated_data["chart"],
                query_arguments=validated_data["query_arguments"],
            )
        except ShortURL.DoesNotExist:
            return super().create(validated_data)

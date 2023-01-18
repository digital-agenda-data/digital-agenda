# Generated by Django 4.1.4 on 2023-01-17 14:42

import digital_agenda.apps.estat.models
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GeoGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    django.contrib.postgres.fields.citext.CICharField(
                        max_length=60, unique=True
                    ),
                ),
                ("size", models.PositiveIntegerField()),
                ("note", models.CharField(blank=True, max_length=1024, null=True)),
                ("geo_codes", models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name="ImportConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    django.contrib.postgres.fields.citext.CICharField(max_length=60),
                ),
                ("title", models.CharField(blank=True, max_length=1024, null=True)),
                ("last_import_time", models.TimeField(null=True)),
                (
                    "indicator",
                    django.contrib.postgres.fields.citext.CICharField(max_length=60),
                ),
                ("indicator_is_surrogate", models.BooleanField(default=False)),
                (
                    "breakdown",
                    django.contrib.postgres.fields.citext.CICharField(max_length=60),
                ),
                ("breakdown_is_surrogate", models.BooleanField(default=False)),
                (
                    "country",
                    django.contrib.postgres.fields.citext.CICharField(
                        default="geo", max_length=60
                    ),
                ),
                ("country_is_surrogate", models.BooleanField(default=False)),
                (
                    "unit",
                    django.contrib.postgres.fields.citext.CICharField(
                        default="unit", max_length=60
                    ),
                ),
                ("unit_is_surrogate", models.BooleanField(default=False)),
                (
                    "period",
                    django.contrib.postgres.fields.citext.CICharField(
                        default="time", max_length=60
                    ),
                ),
                ("period_is_surrogate", models.BooleanField(default=False)),
                (
                    "period_start",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Only include datapoints for periods greater than or equal to this year",
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1990)],
                    ),
                ),
                (
                    "period_end",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Only include datapoints for periods less than or equal to this year",
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1990)],
                    ),
                ),
                ("filters", models.JSONField(blank=True, default=dict)),
                (
                    "mappings",
                    models.JSONField(
                        blank=True,
                        default=digital_agenda.apps.estat.models.default_mappings,
                    ),
                ),
                ("status", models.TextField()),
                (
                    "country_group",
                    models.ForeignKey(
                        blank=True,
                        help_text="Only include datapoints for countries in this group OR the group itself",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="estat.geogroup",
                    ),
                ),
            ],
        ),
    ]

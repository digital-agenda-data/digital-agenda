# Generated by Django 4.1.3 on 2022-11-29 10:23

import ckeditor.fields
import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0005_country_color"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChartGroup",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "display_order",
                    models.PositiveIntegerField(db_index=True, default=100000),
                ),
                (
                    "is_draft",
                    models.BooleanField(
                        default=False,
                        help_text="Draft items will only be visible for admins.",
                    ),
                ),
                (
                    "code",
                    django.contrib.postgres.fields.citext.CICharField(
                        max_length=60, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=40)),
                ("description", ckeditor.fields.RichTextField()),
                ("image", models.ImageField(blank=True, upload_to="")),
                ("indicator_groups", models.ManyToManyField(to="core.indicatorgroup")),
                (
                    "periods",
                    models.ManyToManyField(
                        blank=True,
                        db_table="chart_group_periods",
                        help_text="Limit chart group to the specified periods. If none are specified ALL available periods are used instead.",
                        to="core.period",
                    ),
                ),
            ],
            options={
                "db_table": "chart_groups",
                "ordering": ["display_order", "code"],
            },
        ),
        migrations.CreateModel(
            name="Chart",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "display_order",
                    models.PositiveIntegerField(db_index=True, default=100000),
                ),
                (
                    "is_draft",
                    models.BooleanField(
                        default=False,
                        help_text="Draft items will only be visible for admins.",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("code", models.SlugField(unique=True)),
                (
                    "chart_type",
                    models.CharField(
                        choices=[
                            (
                                "Column",
                                (
                                    (
                                        "COLUMN_COMPARE_COUNTRIES",
                                        "Column Chart: Compare Countries",
                                    ),
                                    (
                                        "COLUMN_COMPARE_BREAKDOWNS",
                                        "Column Chart: Compare Breakdowns",
                                    ),
                                ),
                            ),
                            (
                                "Spline",
                                (
                                    (
                                        "SPLINE_COMPARE_COUNTRIES",
                                        "Spline Chart: Compare Countries",
                                    ),
                                    (
                                        "SPLINE_COMPARE_BREAKDOWNS",
                                        "Spline Chart: Compare Breakdowns",
                                    ),
                                ),
                            ),
                            (
                                "Scatter",
                                (
                                    (
                                        "SCATTER_COMPARE_TWO_INDICATORS",
                                        "Scatter Chart: Compare Two Indicators",
                                    ),
                                ),
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                ("description", ckeditor.fields.RichTextField()),
                (
                    "chart_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="charts.chartgroup",
                    ),
                ),
            ],
            options={
                "db_table": "charts",
                "ordering": ["display_order", "code"],
            },
        ),
    ]

# Generated by Django 4.2.11 on 2024-06-17 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charts", "0023_extrachartnote_hide_from_line_charts"),
    ]

    operations = [
        migrations.AddField(
            model_name="breakdownchartoption",
            name="data_labels_enabled",
            field=models.BooleanField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.dataLabels.enabled",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="breakdownchartoption",
            name="line_width",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.series.lineWidth",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="breakdownchartoption",
            name="marker_enabled",
            field=models.BooleanField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.marker.enabled",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="breakdownchartoption",
            name="marker_radius",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.marker.radius",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="indicatorchartoption",
            name="data_labels_enabled",
            field=models.BooleanField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.dataLabels.enabled",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="indicatorchartoption",
            name="line_width",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.series.lineWidth",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="indicatorchartoption",
            name="marker_enabled",
            field=models.BooleanField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.marker.enabled",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="indicatorchartoption",
            name="marker_radius",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="https://api.highcharts.com/highcharts/plotOptions.spline.marker.radius",
                null=True,
            ),
        ),
    ]

# Generated by Django 4.2.10 on 2024-02-12 12:23

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("charts", "0016_extrachartnote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="breakdownchartoption",
            name="color",
            field=colorfield.fields.ColorField(
                blank=True,
                default=None,
                help_text="Color used for this indicator chart series",
                image_field=None,
                max_length=25,
                null=True,
                samples=None,
            ),
        ),
        migrations.AlterField(
            model_name="indicatorchartoption",
            name="color",
            field=colorfield.fields.ColorField(
                blank=True,
                default=None,
                help_text="Color used for this indicator chart series",
                image_field=None,
                max_length=25,
                null=True,
                samples=None,
            ),
        ),
    ]

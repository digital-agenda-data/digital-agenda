# Generated by Django 4.2.10 on 2024-02-12 12:23

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_indicator_time_coverage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="color",
            field=colorfield.fields.ColorField(
                default="#CCCCCC",
                help_text="Color used for this countries chart series",
                image_field=None,
                max_length=25,
                samples=None,
            ),
        ),
    ]

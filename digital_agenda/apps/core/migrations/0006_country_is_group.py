# Generated by Django 4.1.3 on 2022-12-09 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_country_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="is_group",
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_country_is_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fact",
            name="flags",
            field=models.CharField(blank=True, max_length=12),
        ),
    ]

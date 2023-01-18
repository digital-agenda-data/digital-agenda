# Generated by Django 4.1.4 on 2023-01-17 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("estat", "0001_initial"),
        ("core", "0007_alter_fact_flags"),
    ]

    operations = [
        migrations.AddField(
            model_name="fact",
            name="import_config",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="facts",
                to="estat.importconfig",
            ),
        ),
    ]

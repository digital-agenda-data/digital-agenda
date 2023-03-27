# Generated by Django 4.1.7 on 2023-03-01 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_alter_fact_import_config"),
    ]

    operations = [
        migrations.AddField(
            model_name="fact",
            name="import_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="facts",
                to="core.datafileimport",
            ),
        ),
    ]
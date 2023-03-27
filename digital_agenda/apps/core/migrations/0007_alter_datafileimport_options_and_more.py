# Generated by Django 4.1.7 on 2023-03-27 09:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_remove_datafileimport_errors_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datafileimport",
            options={
                "verbose_name": "Upload data from file",
                "verbose_name_plural": "Upload data from file",
            },
        ),
        migrations.AlterModelOptions(
            name="datafileimporttask",
            options={
                "get_latest_by": "created_on",
                "verbose_name": "Upload file result",
                "verbose_name_plural": "Upload file results",
            },
        ),
    ]

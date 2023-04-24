# Generated by Django 4.2 on 2023-04-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("estat", "0010_importconfig_new_version_available"),
    ]

    operations = [
        migrations.AddField(
            model_name="importconfig",
            name="remarks",
            field=models.TextField(
                blank=True, help_text="Additional notes/remarks", null=True
            ),
        ),
    ]

# Generated by Django 4.2 on 2023-04-05 06:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_create_ci_collation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="breakdown",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="breakdowngroup",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="datasource",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="indicator",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="indicatorgroup",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="code",
            field=models.CharField(
                db_collation="case_insensitive", max_length=60, unique=True
            ),
        ),
    ]

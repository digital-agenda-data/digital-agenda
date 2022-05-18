# Generated by Django 4.0.4 on 2022-05-16 07:38

import django.contrib.postgres.fields.citext
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_dashboard_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
            ],
            options={
                'db_table': 'breakdowns',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'db_table': 'countries',
            },
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_sources',
            },
        ),
        migrations.CreateModel(
            name='DataSourceReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='core.datasource')),
            ],
            options={
                'db_table': 'data_source_refs',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('breakdowns', models.ManyToManyField(db_table='indicators_breakdowns', related_name='indicators', to='core.breakdown')),
                ('countries', models.ManyToManyField(db_table='indicators_countries', related_name='indicators', to='core.country')),
                ('data_source_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='core.datasourcereference')),
            ],
            options={
                'db_table': 'indicators',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
            ],
            options={
                'db_table': 'periods',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
            ],
            options={
                'db_table': 'units',
            },
        ),
        migrations.CreateModel(
            name='IndicatorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('indicators', models.ManyToManyField(db_table='indicators_groups', related_name='groups', to='core.indicator')),
            ],
            options={
                'db_table': 'indicator_groups',
            },
        ),
        migrations.AddField(
            model_name='indicator',
            name='periods',
            field=models.ManyToManyField(db_table='indicators_periods', related_name='indicators', to='core.period'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='units',
            field=models.ManyToManyField(db_table='indicators_units', related_name='indicators', to='core.unit'),
        ),
        migrations.CreateModel(
            name='Fact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('flags', models.CharField(blank=True, max_length=2)),
                ('breakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='core.breakdown')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='core.country')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='core.indicator')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='core.period')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facts', to='core.unit')),
            ],
            options={
                'db_table': 'facts',
            },
        ),
        migrations.CreateModel(
            name='BreakdownGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('breakdowns', models.ManyToManyField(db_table='breakdowns_groups', related_name='groups', to='core.breakdown')),
            ],
            options={
                'db_table': 'breakdown_groups',
            },
        ),
        migrations.AddConstraint(
            model_name='fact',
            constraint=models.CheckConstraint(check=models.Q(('value__isnull', False), models.Q(('flags', ''), _negated=True), _connector='OR'), name='core_fact_either_val_or_flags'),
        ),
        migrations.AlterUniqueTogether(
            name='fact',
            unique_together={('indicator', 'breakdown', 'unit', 'country', 'period')},
        ),
        migrations.AlterUniqueTogether(
            name='datasourcereference',
            unique_together={('data_source', 'name')},
        ),
    ]

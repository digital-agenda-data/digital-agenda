# Generated by Django 4.0.4 on 2022-05-27 05:52

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
                ('definition', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'breakdowns',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='BreakdownGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
                ('display_order', models.PositiveIntegerField(db_index=True, default=100000)),
            ],
            options={
                'db_table': 'breakdown_groups',
                'ordering': ['display_order', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'db_table': 'countries',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_sources',
                'ordering': ['code'],
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
                ('breakdowns', models.ManyToManyField(blank=True, db_table='indicators_breakdowns', related_name='indicators', to='core.breakdown')),
                ('countries', models.ManyToManyField(blank=True, db_table='indicators_countries', related_name='indicators', to='core.country')),
                ('data_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='core.datasource')),
            ],
            options={
                'db_table': 'indicators',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='IndicatorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
                ('display_order', models.PositiveIntegerField(db_index=True, default=100000)),
            ],
            options={
                'db_table': 'indicator_groups',
                'ordering': ['display_order', 'code'],
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'periods',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', django.contrib.postgres.fields.citext.CICharField(max_length=60, unique=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('alt_label', models.TextField(blank=True, null=True, verbose_name='Alt. label')),
                ('definition', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'units',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='IndicatorGroupLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.PositiveIntegerField(db_index=True, default=100000)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.indicatorgroup')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.indicator')),
            ],
            options={
                'verbose_name': 'indicator',
                'verbose_name_plural': 'membership',
                'db_table': 'indicators_groups',
                'ordering': ['display_order'],
                'unique_together': {('indicator', 'group')},
            },
        ),
        migrations.AddField(
            model_name='indicatorgroup',
            name='indicators',
            field=models.ManyToManyField(blank=True, related_name='groups', through='core.IndicatorGroupLink', to='core.indicator'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='periods',
            field=models.ManyToManyField(blank=True, db_table='indicators_periods', related_name='indicators', to='core.period'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='units',
            field=models.ManyToManyField(blank=True, db_table='indicators_units', related_name='indicators', to='core.unit'),
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
            name='BreakdownGroupLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.PositiveIntegerField(db_index=True, default=100000)),
                ('breakdown', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.breakdown')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.breakdowngroup')),
            ],
            options={
                'verbose_name': 'breakdown',
                'verbose_name_plural': 'membership',
                'db_table': 'breakdowns_groups',
                'ordering': ['display_order'],
            },
        ),
        migrations.AddField(
            model_name='breakdowngroup',
            name='breakdowns',
            field=models.ManyToManyField(blank=True, related_name='groups', through='core.BreakdownGroupLink', to='core.breakdown'),
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
            name='breakdowngrouplink',
            unique_together={('breakdown', 'group')},
        ),
    ]

# Generated by Django 3.2.9 on 2023-04-18 18:29

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNotification',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='Created at')),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Updated at')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Notification',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalState',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='Created at')),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical State',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name_en')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description_en')),
                ('name_pt', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name_pt')),
                ('description_pt', models.TextField(blank=True, null=True, verbose_name='Description_pt')),
            ],
            options={
                'verbose_name': 'List item',
                'verbose_name_plural': 'List items',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ListType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name_en')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description_en')),
                ('name_pt', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name_pt')),
                ('description_pt', models.TextField(blank=True, null=True, verbose_name='Description_pt')),
            ],
            options={
                'verbose_name': 'List type',
                'verbose_name_plural': 'Types of lists',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active_status', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
                'ordering': ['-created'],
            },
        ),
    ]

# Generated by Django 5.0 on 2024-07-13 11:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RollQue',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('deeds_town', models.IntegerField()),
                ('suburb', models.IntegerField()),
                ('scheme', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ValuationRoll',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rate_number', models.IntegerField()),
                ('legal_description', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('suburb', models.CharField(max_length=55)),
                ('deeds_town', models.CharField(max_length=55)),
                ('scheme', models.CharField(max_length=55)),
                ('first_owner', models.CharField(max_length=125)),
                ('use_code', models.CharField(max_length=55)),
                ('rating_category', models.CharField(max_length=55)),
                ('market_value', models.CharField(max_length=55)),
                ('registered_extent', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('roll_type', models.CharField(max_length=55)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]

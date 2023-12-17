# Generated by Django 4.2.4 on 2023-11-03 01:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='regi_content',
            fields=[
                ('control_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('total_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('name_id', models.IntegerField(default=0)),
                ('company_name', models.CharField(max_length=255)),
                ('q_contents', models.TextField()),
                ('a_contents', models.TextField()),
                ('unsolved', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('user_ip', models.GenericIPAddressField(unique=True)),
            ],
        ),
    ]

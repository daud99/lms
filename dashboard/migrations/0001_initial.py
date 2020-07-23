# Generated by Django 2.2.14 on 2020-07-23 13:10

import dashboard.forms
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=155)),
                ('courses', dashboard.forms.CustomDictField(blank=True, default={}, null=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.College')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]

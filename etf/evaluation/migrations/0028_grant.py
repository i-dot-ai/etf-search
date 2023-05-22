# Generated by Django 3.2.18 on 2023-05-10 22:29

import uuid

import django.db.models.deletion
from django.db import migrations, models

import etf.evaluation.models


class Migration(migrations.Migration):
    dependencies = [
        ("evaluation", "0027_rename_status_evaluation_visibility"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name_of_grant", models.CharField(blank=True, max_length=256, null=True)),
                ("grant_number", models.CharField(blank=True, max_length=256, null=True)),
                ("grant_details", models.TextField(blank=True, null=True)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="grants", to="evaluation.evaluation"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(etf.evaluation.models.NamedModel, models.Model),
        ),
    ]

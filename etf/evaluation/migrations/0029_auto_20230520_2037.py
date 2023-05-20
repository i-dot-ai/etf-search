# Generated by Django 3.2.18 on 2023-05-20 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("evaluation", "0028_processevaluationaspect_processevaluationmethod"),
    ]

    operations = [
        migrations.AddField(
            model_name="processevaluationmethod",
            name="aspects_measured",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="processevaluationmethod",
            name="more_information",
            field=models.TextField(blank=True, null=True),
        ),
    ]

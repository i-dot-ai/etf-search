# Generated by Django 3.2.16 on 2023-01-20 14:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("evaluation", "0006_auto_20230120_1342"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="evaluation",
            name="doi",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="rap_outcome",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="rap_outcome_detail",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="rap_planned",
        ),
        migrations.RemoveField(
            model_name="evaluation",
            name="rap_planned_detail",
        ),
    ]

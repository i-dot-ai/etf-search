# Generated by Django 3.2.16 on 2022-10-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rbca", "0003_alter_application_locations"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="name",
            field=models.CharField(blank=True, max_length=127, null=True),
        ),
    ]

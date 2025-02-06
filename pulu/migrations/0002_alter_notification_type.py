# Generated by Django 4.2.18 on 2025-02-06 14:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pulu", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="type",
            field=models.IntegerField(
                choices=[(20, "Information"), (30, "Alert"), (40, "Error")],
                default=20,
                verbose_name="Notification type",
            ),
        ),
    ]

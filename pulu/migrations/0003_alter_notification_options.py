# Generated by Django 4.2.18 on 2025-02-06 15:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pulu", "0002_alter_notification_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={
                "ordering": ["-type", "-validity_period_start", "-created_at"],
                "verbose_name": "notification",
                "verbose_name_plural": "notifications",
            },
        ),
    ]

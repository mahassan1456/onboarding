# Generated by Django 4.1.7 on 2023-03-20 01:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0009_rename_modified_at_historicalhospital2_updated_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalhospital2",
            name="is_manual_time",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name="hospital2",
            name="is_manual_time",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]

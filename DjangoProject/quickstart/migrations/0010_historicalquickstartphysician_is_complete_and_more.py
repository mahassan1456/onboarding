# Generated by Django 4.1.7 on 2023-03-20 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quickstart", "0009_historicalquickstartphysician_is_new_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalquickstartphysician",
            name="is_complete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="quickstartphysician",
            name="is_complete",
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.1.6 on 2023-03-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quickstart", "0002_remove_quickstarthospital1_hospital_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="quickstarthospital1",
            name="hospital_address",
            field=models.CharField(default="", max_length=60, null=True),
        ),
    ]

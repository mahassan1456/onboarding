# Generated by Django 4.1.6 on 2023-03-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quickstart", "0005_alter_quickstarthospital1_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quickstarthospital1",
            name="has_physicians",
            field=models.BooleanField(default=False),
        ),
    ]

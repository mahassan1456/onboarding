# Generated by Django 4.1.6 on 2023-03-10 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0002_historicalhospital2_physicians_onboarded_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalhospital2",
            name="soft_delete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="hospital2",
            name="soft_delete",
            field=models.BooleanField(default=False),
        ),
    ]

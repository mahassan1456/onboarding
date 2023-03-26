# Generated by Django 4.1.6 on 2023-03-15 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0005_historicalhospital2_email_hospital2_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalhospital2",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name="hospital2",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=60, null=True),
        ),
    ]
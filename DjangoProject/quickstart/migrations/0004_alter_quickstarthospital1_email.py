# Generated by Django 4.1.6 on 2023-03-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quickstart", "0003_quickstarthospital1_hospital_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quickstarthospital1",
            name="email",
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
    ]
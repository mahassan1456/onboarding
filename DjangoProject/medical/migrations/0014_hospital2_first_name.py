# Generated by Django 4.1.7 on 2023-03-25 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0013_alter_hospital2_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital2",
            name="first_name",
            field=models.CharField(default="", max_length=40, null=True),
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-17 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0006_alter_historicalhospital2_email_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="hospital2",
            options={"ordering": ["-created_at"]},
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-17 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0006_alter_userhistorytable_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="userhistorytable",
            name="page_link2",
            field=models.CharField(default="", max_length=64, null=True),
        ),
    ]

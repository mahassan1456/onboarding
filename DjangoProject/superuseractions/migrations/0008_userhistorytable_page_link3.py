# Generated by Django 4.1.7 on 2023-03-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0007_userhistorytable_page_link2"),
    ]

    operations = [
        migrations.AddField(
            model_name="userhistorytable",
            name="page_link3",
            field=models.CharField(default="", max_length=64, null=True),
        ),
    ]

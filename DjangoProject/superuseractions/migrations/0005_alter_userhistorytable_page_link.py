# Generated by Django 4.1.7 on 2023-03-16 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0004_userhistorytable_page_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userhistorytable",
            name="page_link",
            field=models.CharField(default="", max_length=64, null=True),
        ),
    ]

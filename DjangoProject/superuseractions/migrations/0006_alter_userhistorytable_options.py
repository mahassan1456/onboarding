# Generated by Django 4.1.7 on 2023-03-17 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0005_alter_userhistorytable_page_link"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="userhistorytable",
            options={"ordering": ["-action_time"]},
        ),
    ]

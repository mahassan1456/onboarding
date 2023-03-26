# Generated by Django 4.1.7 on 2023-03-20 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0010_remove_userhistorytable_age_link3_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userhistorytable",
            name="action",
            field=models.CharField(
                choices=[
                    ("1", "Create"),
                    ("2", "Update"),
                    ("0", "Delete"),
                    ("3", "Restored"),
                ],
                max_length=1,
            ),
        ),
    ]
# Generated by Django 4.1.7 on 2023-03-25 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0016_rename_first_name_hospital2_admin_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital2",
            name="admin_name_1",
            field=models.CharField(default="", max_length=40, null=True),
        ),
    ]

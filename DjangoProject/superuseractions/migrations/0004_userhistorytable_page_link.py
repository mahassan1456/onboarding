# Generated by Django 4.1.7 on 2023-03-16 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("superuseractions", "0003_alter_userhistorytable_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="userhistorytable",
            name="page_link",
            field=models.SlugField(null=True),
        ),
    ]

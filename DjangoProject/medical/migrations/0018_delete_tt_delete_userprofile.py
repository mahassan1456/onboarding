# Generated by Django 4.1.7 on 2023-03-26 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0017_hospital2_admin_name_1"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TT",
        ),
        migrations.DeleteModel(
            name="userProfile",
        ),
    ]
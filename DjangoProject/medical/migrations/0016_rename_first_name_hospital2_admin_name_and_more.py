# Generated by Django 4.1.7 on 2023-03-25 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medical", "0015_hospital2_last_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="hospital2",
            old_name="first_name",
            new_name="admin_name",
        ),
        migrations.RemoveField(
            model_name="hospital2",
            name="last_name",
        ),
    ]

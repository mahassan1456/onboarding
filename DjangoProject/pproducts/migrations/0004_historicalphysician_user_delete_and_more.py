# Generated by Django 4.1.6 on 2023-03-10 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pproducts", "0003_historicalproduct_soft_delete_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalphysician",
            name="user_delete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="physician",
            name="user_delete",
            field=models.BooleanField(default=False),
        ),
    ]

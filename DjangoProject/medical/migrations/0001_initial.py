# Generated by Django 4.1.6 on 2023-03-05 21:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import medical.utility_functions
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=20)),
                ("age", models.IntegerField(default="")),
                ("hobbies", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="userProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mobile_contact",
                    models.CharField(
                        default="",
                        max_length=12,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Please input a Contact number in a Valid Format e.g 713-293-0949",
                                regex="[0-9]{3}-[0-9]{3}-[0-9]{4}",
                            )
                        ],
                    ),
                ),
                (
                    "job_title",
                    models.CharField(
                        default="N/A",
                        max_length=40,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="Please input a Position of at least 2 chracters",
                            )
                        ],
                    ),
                ),
                (
                    "additional_information",
                    models.TextField(default=" ", max_length=250),
                ),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hospital2",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=medical.utility_functions.user_directory_path_hospital,
                    ),
                ),
                ("name", models.TextField(default="", max_length=50)),
                ("taxid", models.CharField(default="", max_length=10, null=True)),
                ("bankaccount", models.CharField(default="", max_length=17, null=True)),
                ("routing", models.CharField(default="", max_length=9)),
                ("street", models.TextField(default="", max_length=100)),
                ("city", models.TextField(default="", max_length=50)),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Please Select a State"),
                            ("AL", "Alabama"),
                            ("AK", "Alaska"),
                            ("AS", "American Samoa"),
                            ("AZ", "Arizona"),
                            ("AR", "Arkansas"),
                            ("CA", "California"),
                            ("CO", "Colorado"),
                            ("CT", "Connecticut"),
                            ("DE", "Delaware"),
                            ("DC", "District of Columbia"),
                            ("FL", "Florida"),
                            ("GA", "Georgia"),
                            ("GU", "Guam"),
                            ("HI", "Hawaii"),
                            ("ID", "Idaho"),
                            ("IL", "Illinois"),
                            ("IN", "Indiana"),
                            ("IA", "Iowa"),
                            ("KS", "Kansas"),
                            ("KY", "Kentucky"),
                            ("LA", "Louisiana"),
                            ("ME", "Maine"),
                            ("MD", "Maryland"),
                            ("MA", "Massachusetts"),
                            ("MI", "Michigan"),
                            ("MN", "Minnesota"),
                            ("MS", "Mississippi"),
                            ("MO", "Missouri"),
                            ("MT", "Montana"),
                            ("NE", "Nebraska"),
                            ("NV", "Nevada"),
                            ("NH", "New Hampshire"),
                            ("NJ", "New Jersey"),
                            ("NM", "New Mexico"),
                            ("NY", "New York"),
                            ("NC", "North Carolina"),
                            ("ND", "North Dakota"),
                            ("MP", "Northern Mariana Islands"),
                            ("OH", "Ohio"),
                            ("OK", "Oklahoma"),
                            ("OR", "Oregon"),
                            ("PA", "Pennsylvania"),
                            ("PR", "Puerto Rico"),
                            ("RI", "Rhode Island"),
                            ("SC", "South Carolina"),
                            ("SD", "South Dakota"),
                            ("TN", "Tennessee"),
                            ("TX", "Texas"),
                            ("UT", "Utah"),
                            ("VT", "Vermont"),
                            ("VI", "Virgin Islands"),
                            ("VA", "Virginia"),
                            ("WA", "Washington"),
                            ("WV", "West Virginia"),
                            ("WI", "Wisconsin"),
                            ("WY", "Wyoming"),
                        ],
                        default="",
                        max_length=5,
                    ),
                ),
                ("zip", models.TextField(default="", max_length=5, null=True)),
                ("phone", models.CharField(default="", max_length=12, null=True)),
                ("total_physicians", models.IntegerField(blank=True, null=True)),
                ("website", models.CharField(default="", max_length=50)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_manual", models.BooleanField(default=False)),
                ("prompt_credentials", models.BooleanField(default=False)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "approved_by",
                    models.CharField(blank=True, default="", max_length=35),
                ),
                ("has_physicians", models.BooleanField(default=False)),
                ("has_administrator", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hospitals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="HistoricalHospital2",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("picture", models.TextField(blank=True, max_length=100, null=True)),
                ("name", models.TextField(default="", max_length=50)),
                ("taxid", models.CharField(default="", max_length=10, null=True)),
                ("bankaccount", models.CharField(default="", max_length=17, null=True)),
                ("routing", models.CharField(default="", max_length=9)),
                ("street", models.TextField(default="", max_length=100)),
                ("city", models.TextField(default="", max_length=50)),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("", "Please Select a State"),
                            ("AL", "Alabama"),
                            ("AK", "Alaska"),
                            ("AS", "American Samoa"),
                            ("AZ", "Arizona"),
                            ("AR", "Arkansas"),
                            ("CA", "California"),
                            ("CO", "Colorado"),
                            ("CT", "Connecticut"),
                            ("DE", "Delaware"),
                            ("DC", "District of Columbia"),
                            ("FL", "Florida"),
                            ("GA", "Georgia"),
                            ("GU", "Guam"),
                            ("HI", "Hawaii"),
                            ("ID", "Idaho"),
                            ("IL", "Illinois"),
                            ("IN", "Indiana"),
                            ("IA", "Iowa"),
                            ("KS", "Kansas"),
                            ("KY", "Kentucky"),
                            ("LA", "Louisiana"),
                            ("ME", "Maine"),
                            ("MD", "Maryland"),
                            ("MA", "Massachusetts"),
                            ("MI", "Michigan"),
                            ("MN", "Minnesota"),
                            ("MS", "Mississippi"),
                            ("MO", "Missouri"),
                            ("MT", "Montana"),
                            ("NE", "Nebraska"),
                            ("NV", "Nevada"),
                            ("NH", "New Hampshire"),
                            ("NJ", "New Jersey"),
                            ("NM", "New Mexico"),
                            ("NY", "New York"),
                            ("NC", "North Carolina"),
                            ("ND", "North Dakota"),
                            ("MP", "Northern Mariana Islands"),
                            ("OH", "Ohio"),
                            ("OK", "Oklahoma"),
                            ("OR", "Oregon"),
                            ("PA", "Pennsylvania"),
                            ("PR", "Puerto Rico"),
                            ("RI", "Rhode Island"),
                            ("SC", "South Carolina"),
                            ("SD", "South Dakota"),
                            ("TN", "Tennessee"),
                            ("TX", "Texas"),
                            ("UT", "Utah"),
                            ("VT", "Vermont"),
                            ("VI", "Virgin Islands"),
                            ("VA", "Virginia"),
                            ("WA", "Washington"),
                            ("WV", "West Virginia"),
                            ("WI", "Wisconsin"),
                            ("WY", "Wyoming"),
                        ],
                        default="",
                        max_length=5,
                    ),
                ),
                ("zip", models.TextField(default="", max_length=5, null=True)),
                ("phone", models.CharField(default="", max_length=12, null=True)),
                ("total_physicians", models.IntegerField(blank=True, null=True)),
                ("website", models.CharField(default="", max_length=50)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified_at", models.DateTimeField(blank=True, editable=False)),
                ("is_manual", models.BooleanField(default=False)),
                ("prompt_credentials", models.BooleanField(default=False)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "approved_by",
                    models.CharField(blank=True, default="", max_length=35),
                ),
                ("has_physicians", models.BooleanField(default=False)),
                ("has_administrator", models.BooleanField(default=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical hospital2",
                "verbose_name_plural": "historical hospital2s",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

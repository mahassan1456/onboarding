# Generated by Django 4.1.6 on 2023-03-05 22:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import login.utility_functions
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WaitingRoom",
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
                ("zip", models.TextField(default="", max_length=12)),
                ("total_physicians", models.IntegerField(blank=True, null=True)),
                ("website", models.CharField(default="", max_length=50)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "approved_by",
                    models.CharField(blank=True, default="", max_length=35),
                ),
            ],
        ),
        migrations.CreateModel(
            name="userProfileAdmin",
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
                        upload_to=login.utility_functions.user_profile_picture_directory_path,
                    ),
                ),
                (
                    "mobile_contact",
                    models.CharField(
                        default="",
                        max_length=12,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=10,
                                message="Please Input a value between 10 and 13 digits(if formatted w/ dashes)",
                            ),
                            django.core.validators.MaxLengthValidator(
                                limit_value=13,
                                message="Please Input a value between 10 and 13 digits(if formatted w/ dashes",
                            ),
                        ],
                    ),
                ),
                (
                    "job_title",
                    models.CharField(
                        default="",
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
                    models.TextField(blank=True, default=" ", max_length=250),
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
            name="HistoricalWaitingRoom",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
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
                ("zip", models.TextField(default="", max_length=12)),
                ("total_physicians", models.IntegerField(blank=True, null=True)),
                ("website", models.CharField(default="", max_length=50)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("modified_at", models.DateTimeField(blank=True, editable=False)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                (
                    "approved_by",
                    models.CharField(blank=True, default="", max_length=35),
                ),
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
            ],
            options={
                "verbose_name": "historical waiting room",
                "verbose_name_plural": "historical waiting rooms",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricaluserProfileAdmin",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("picture", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "mobile_contact",
                    models.CharField(
                        default="",
                        max_length=12,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=10,
                                message="Please Input a value between 10 and 13 digits(if formatted w/ dashes)",
                            ),
                            django.core.validators.MaxLengthValidator(
                                limit_value=13,
                                message="Please Input a value between 10 and 13 digits(if formatted w/ dashes",
                            ),
                        ],
                    ),
                ),
                (
                    "job_title",
                    models.CharField(
                        default="",
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
                    models.TextField(blank=True, default=" ", max_length=250),
                ),
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
                "verbose_name": "historical user profile admin",
                "verbose_name_plural": "historical user profile admins",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
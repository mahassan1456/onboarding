# Generated by Django 4.1.6 on 2023-03-05 21:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pproducts.fields
import quickstart.utility_functions
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pproducts", "0001_initial"),
        ("medical", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="quickStartHospital1",
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
                    "hospital_name",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "hospital_zip",
                    models.EmailField(default="", max_length=40, null=True),
                ),
                (
                    "hospital_address",
                    models.CharField(default="", max_length=60, null=True),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="This field must have a minimum of 2 characters",
                            )
                        ],
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="This field must have a minimum of 2 characters",
                            )
                        ],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=50,
                        null=True,
                        validators=[
                            django.core.validators.EmailValidator(
                                message="Please input email address in the proper format."
                            )
                        ],
                    ),
                ),
                (
                    "phone",
                    models.CharField(blank=True, default="", max_length=12, null=True),
                ),
                (
                    "additional",
                    models.TextField(blank=True, default="", max_length=250),
                ),
                ("email_message", models.TextField(default="", max_length=512)),
                ("is_emailed", models.BooleanField(default=False)),
                ("is_registered", models.BooleanField(default=False)),
                ("number_emails_sent", models.IntegerField(default=0)),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="qs_hospital",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="quickStartPhysician",
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
                    "hospital_type",
                    models.CharField(
                        choices=[
                            ("new", "New Hospital"),
                            ("invite", "Recently Invited"),
                            ("onboarded", "Fully Onboarded"),
                            ("na", "Don't Assign"),
                        ],
                        default="",
                        max_length=25,
                    ),
                ),
                (
                    "hospital_name",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "first_name",
                    models.CharField(
                        default="",
                        max_length=50,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="This field must have a minimum of 2 characters",
                            )
                        ],
                    ),
                ),
                ("last_name", models.CharField(default="", max_length=50)),
                ("email", models.EmailField(max_length=50)),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("email_message", models.TextField(default="", max_length=512)),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=quickstart.utility_functions.user_directory_path_QS_physicians,
                    ),
                ),
                ("description", models.TextField(default="", max_length=512)),
                ("is_assigned", models.BooleanField(default=False)),
                ("is_emailed", models.BooleanField(default=False)),
                ("is_onboarded", models.BooleanField(default=False)),
                ("is_recommending", models.BooleanField(default=False)),
                ("products", pproducts.fields.MyJsonField(blank=True, null=True)),
                ("about_me", models.TextField(default="", max_length=512)),
                (
                    "hospital",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical.hospital2",
                    ),
                ),
                (
                    "hospital_invite",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="qs_physicians",
                        to="quickstart.quickstarthospital1",
                    ),
                ),
                (
                    "specialty",
                    models.ManyToManyField(null=True, to="pproducts.producttags"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalquickStartPhysician",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "hospital_type",
                    models.CharField(
                        choices=[
                            ("new", "New Hospital"),
                            ("invite", "Recently Invited"),
                            ("onboarded", "Fully Onboarded"),
                            ("na", "Don't Assign"),
                        ],
                        default="",
                        max_length=25,
                    ),
                ),
                (
                    "hospital_name",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "first_name",
                    models.CharField(
                        default="",
                        max_length=50,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                limit_value=2,
                                message="This field must have a minimum of 2 characters",
                            )
                        ],
                    ),
                ),
                ("last_name", models.CharField(default="", max_length=50)),
                ("email", models.EmailField(max_length=50)),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                ("email_message", models.TextField(default="", max_length=512)),
                ("picture", models.TextField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(default="", max_length=512)),
                ("is_assigned", models.BooleanField(default=False)),
                ("is_emailed", models.BooleanField(default=False)),
                ("is_onboarded", models.BooleanField(default=False)),
                ("is_recommending", models.BooleanField(default=False)),
                ("products", pproducts.fields.MyJsonField(blank=True, null=True)),
                ("about_me", models.TextField(default="", max_length=512)),
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
                    "hospital",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="medical.hospital2",
                    ),
                ),
                (
                    "hospital_invite",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="quickstart.quickstarthospital1",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical quick start physician",
                "verbose_name_plural": "historical quick start physicians",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
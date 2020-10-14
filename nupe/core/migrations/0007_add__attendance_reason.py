# Generated by Django 3.1 on 2020-10-02 19:53

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_add__function__sector"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceReason",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(editable=False, null=True)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(max_length=255)),
                (
                    "father_reason",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sons_reasons",
                        related_query_name="son_reason",
                        to="core.AttendanceReason",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AlterModelManagers(
            name="attendancereason", managers=[("only_father", django.db.models.manager.Manager()),],
        ),
    ]
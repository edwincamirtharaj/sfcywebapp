# Generated by Django 5.0.1 on 2024-02-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0002_department_month_year_reportname_fileupload"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercompanymapping",
            name="is_approved",
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.1.4 on 2023-06-15 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0007_accommodatesurvey_room_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tripsurvey",
            name="rate_of_unknown",
        ),
    ]

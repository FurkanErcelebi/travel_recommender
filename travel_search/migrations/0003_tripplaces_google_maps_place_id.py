# Generated by Django 4.1.4 on 2023-01-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_search', '0002_rename_lable_place_label_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripplaces',
            name='google_maps_place_id',
            field=models.CharField(max_length=27, null=True),
        ),
    ]

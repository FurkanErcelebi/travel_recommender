# Generated by Django 4.1.4 on 2023-04-23 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0006_customer_description_deposit_description_and_more"),
        ("surveys", "0006_remove_personalsurvey_customer_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="accommodatesurvey",
            name="room_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.rooms",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="customer_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.customer",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="deposit_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.deposit",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="distribution_channel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.marketdist",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="hotel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.hotels",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="market_segment",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.marketdist",
            ),
        ),
        migrations.AddField(
            model_name="personalsurvey",
            name="meal",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="utils.meals",
            ),
        ),
    ]

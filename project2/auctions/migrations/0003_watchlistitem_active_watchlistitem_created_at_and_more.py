# Generated by Django 4.2.2 on 2023-06-09 22:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_remove_auctionlisting_current_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlistitem",
            name="active",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="watchlistitem",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="watchlistitem",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
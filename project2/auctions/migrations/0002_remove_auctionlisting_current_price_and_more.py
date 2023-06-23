# Generated by Django 4.2.2 on 2023-06-09 22:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="auctionlisting",
            name="current_price",
        ),
        migrations.AddField(
            model_name="bid",
            name="auction_listing",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.auctionlisting",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bid",
            name="bid_price",
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bid",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]

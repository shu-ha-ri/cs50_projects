# Generated by Django 4.2.2 on 2023-06-09 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_auctionlisting_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionlisting",
            name="active",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]

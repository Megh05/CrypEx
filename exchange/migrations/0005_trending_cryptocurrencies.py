# Generated by Django 5.0b1 on 2023-11-18 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_cryptocurrency_symbol_alter_cryptocurrency_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trending_Cryptocurrencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('price', models.FloatField()),
                ('h24', models.FloatField()),
                ('volume24h', models.BigIntegerField(default=0)),
            ],
        ),
    ]
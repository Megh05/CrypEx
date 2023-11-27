# Generated by Django 4.2.5 on 2023-11-23 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange', '0008_cryptocurrency_total_supply'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCryptoHoldings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holdings', models.JSONField(default=dict)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=6, default=0.0, max_digits=15)),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cryptocurrency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.cryptocurrency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
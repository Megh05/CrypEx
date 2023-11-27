# Generated by Django 4.2.5 on 2023-11-06 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_rename_cryptocurr_cryptocurrency'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='symbol',
            field=models.CharField(default='Btc', max_length=10),
        ),
        migrations.AlterField(
            model_name='cryptocurrency',
            name='name',
            field=models.CharField(default='Bitcoin', max_length=100),
        ),
    ]
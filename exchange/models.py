from django.db import models
from django.contrib.auth.models import User
from .models import *
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

class identityImage(models.Model):
    User = models.OneToOneField(User,on_delete=models.CASCADE)
    identity = models.ImageField(blank=True,upload_to="id/")

    def __str__(self):
        return self.User.username

class Cryptocurrency(models.Model):

    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, default='Btc')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    forecast_1h = models.DecimalField(max_digits=5, decimal_places=2)
    forecast_24h = models.DecimalField(max_digits=5, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=15, decimal_places=2)
    total_supply = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)


    official_site = models.URLField(default='')
    whitepaper = models.URLField(default='')
    github = models.URLField(default='')
    reddit = models.URLField(default='')
    news = models.TextField(default='')
    about = models.TextField(default='')

    class Meta:
        app_label = 'exchange'

    def __str__(self):
        return self.name


class Trending_Cryptocurrencies(models.Model):
    currency_name = models.CharField(max_length=100)
    number = models.IntegerField()
    price = models.FloatField()
    h24 = models.FloatField()
    volume24h = models.BigIntegerField(default=0)

    def __str__(self):
        return self.currency_name


class UserCryptoHoldings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    holdings = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.username}'s Holdings"

    def update_holdings(self, cryptocurrency, amount, transaction_type):
        amount = Decimal(str(amount))  # Convert the amount to Decimal

        if transaction_type == 'buy':
            self.holdings[cryptocurrency] = Decimal(str(self.holdings.get(cryptocurrency, Decimal('0')))) + amount
        elif transaction_type == 'sell':
            if cryptocurrency in self.holdings:
                self.holdings[cryptocurrency] = max(Decimal('0'), Decimal(str(self.holdings[cryptocurrency])) - amount)

        self.save()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, default = 0.000000)
    transaction_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy')
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update user's cryptocurrency holdings
        user_holdings, created = UserCryptoHoldings.objects.get_or_create(user=self.user)
        if self.cryptocurrency.name not in user_holdings.holdings:
            user_holdings.holdings[self.cryptocurrency.name] = 0

        if self.transaction_type == 'buy':
            user_holdings.holdings[self.cryptocurrency.name] += int(self.quantity)  # Convert to int
        elif self.transaction_type == 'sell':
            user_holdings.holdings[self.cryptocurrency.name] -= int(self.quantity)  # Convert to int

        user_holdings.save()

        # Save the transaction
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.quantity} {self.cryptocurrency}"


from django.contrib import admin

from exchange.models import *

# Register your models here.
admin.site.register(Cryptocurrency)
admin.site.register(Trending_Cryptocurrencies)
admin.site.register(Transaction)
admin.site.register(UserCryptoHoldings)
admin.site.register(identityImage)

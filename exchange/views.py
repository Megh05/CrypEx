from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import stripe

stripe.api_key = 'sk_test_51O982oBtZSYWekNB82nFBUxOzSZ5o8xOyD4VJx8OkVjq71J604F7e6iTXAHVRZqr8Q5sjoJfO8xd1HEHRkaxbqd800mLzQLkCe'


def crypto_list(request):
    if not request.user.is_authenticated:
        cryptocurrencies = Cryptocurrency.objects.all()
        return render(request, 'registration/notRegister.html', {'cryptocurrencies': cryptocurrencies})

    currencies = {
        'usd': 1,  # USD conversion rate (base currency)
        'eur': 0.85,  # Conversion rate for EUR from USD
        'cad': 1.25,  # Conversion rate for CAD from USD
        'btc': 0.000022  # Conversion rate for BTC from USD
        # Add more currencies and their conversion rates as needed
    }
    currency_symbols = {
        'Select': '$',
        'usd': '$',
        'eur': '€',
        'cad': 'CA$',
        'btc': 'BTC'
    }

    currency_list = ['USD', 'CAD', 'EUR', 'BTC']
    selected_currency = request.GET.get('currency', 'Select')  # Get selected currency or default to USD
    conversion_rate = currencies.get(selected_currency, 1)  # Get the conversion rate

    cryptocurrencies = Cryptocurrency.objects.all()
    converted_cryptos = []

    for crypto in cryptocurrencies:
        converted_price = float(crypto.price) * conversion_rate
        converted_cryptos.append({'name': crypto.name, 'price': converted_price, 'forecast_1h': crypto.forecast_1h,
                                  'market_cap': crypto.market_cap, 'volume': crypto.volume,
                                  'circulating_supply': crypto.circulating_supply, 'forecast_24h': crypto.forecast_24h,
                                  'id': crypto.id})
    sort_param = request.GET.get('sort', None)
    direction = request.GET.get('direction', 'asc')  # Default to ascending order
    #
    if not sort_param:
        sort_param = 'id'

    sorted_column = request.GET.get('sorted_column', '')
    if sort_param == sorted_column:
        direction = 'desc' if direction == 'asc' else 'asc'
    else:
        direction = 'asc'

    def get_sort_key(converted_cryptos):
        if sort_param == 'name':
            return converted_cryptos['name']
        elif sort_param == 'price':
            return converted_cryptos['price']
        elif sort_param == 'forecast_1h':
            return converted_cryptos['forecast_1h']
        elif sort_param == 'market_cap':
            return converted_cryptos['market_cap']
        elif sort_param == 'volume':
            return converted_cryptos['volume']
        elif sort_param == 'circulating_supply':
            return converted_cryptos['circulating_supply']
        elif sort_param == 'forecast_24h':
            return converted_cryptos['forecast_24h']
        elif sort_param == 'id':
            return converted_cryptos['id']
        else:
            # Default to sorting by name if sort_param is not recognized
            return converted_cryptos['name']

    # Sort the list based on the specified key and direction
    converted_cryptos = sorted(converted_cryptos, key=get_sort_key, reverse=(direction == 'desc'))

    trending_crypto_list = Cryptocurrency.objects.all().order_by('?')[:3]
    most_visited_crypto_list = Cryptocurrency.objects.all().order_by('?')[:3]
    gainers_crypto_list = Cryptocurrency.objects.all().order_by('?')[:3]
    losers_crypto_list = Cryptocurrency.objects.all().order_by('?')[:3]
    recently_added_crypto_list = Cryptocurrency.objects.all().order_by('?')[:3]

    context = {'cryptocurrencies': converted_cryptos,
               'trending_crypto_list': trending_crypto_list,
               'most_visited_crypto_list': most_visited_crypto_list,
               'gainers_crypto_list': gainers_crypto_list,
               'losers_crypto_list': losers_crypto_list,
               'recently_added_crypto_list': recently_added_crypto_list,
               'currency_list': currency_list, 'selected_currency': selected_currency,
               'currency_symbol': currency_symbols[selected_currency], 'sort_param': sort_param,
               'sorted_column': sorted_column, 'direction': direction}

    return render(request, 'exchange/exchange.html',
                  context)


# @login_required
# def details(request):
#     cryptocurrency = Cryptocurrency.objects.get(name='Bitcoin')
#     newsList = cryptocurrency.news.split(",")
#     return render(request, 'exchange/details.html', {'cryptocurrency': cryptocurrency, 'newsList':newsList})

@login_required
def details(request, currency_name):
    currency = Cryptocurrency.objects.get(name=currency_name)
    currencies = {
        'usd': 1,  # USD conversion rate (base currency)
        'eur': 0.85,  # Conversion rate for EUR from USD
        'cad': 1.25,  # Conversion rate for CAD from USD
        'btc': 0.000022  # Conversion rate for BTC from USD
        # Add more currencies and their conversion rates as needed
    }
    currency_symbols = {
        'Select': '$',
        'usd': '$',
        'eur': '€',
        'cad': 'CA$',
        'btc': 'BTC'
    }
    currency_list = ['USD', 'CAD', 'EUR', 'BTC']
    selected_currency = request.GET.get('currency', 'Select')  # Get selected currency or default to USD
    conversion_rate = currencies.get(selected_currency, 1)  # Get the conversion rate

    cryptocurrencies = Cryptocurrency.objects.get(name=currency_name)

    converted_price = float(cryptocurrencies.price) * conversion_rate
    newsList = cryptocurrencies.news.split(",")
    converted_cryptos = (
        {'name': cryptocurrencies.name, 'price': converted_price, 'forecast_1h': cryptocurrencies.forecast_1h,
         'market_cap': cryptocurrencies.market_cap, 'volume': cryptocurrencies.volume,
         'circulating_supply': cryptocurrencies.circulating_supply, 'forecast_24h': cryptocurrencies.forecast_24h,
         'id': cryptocurrencies.id, 'symbol': cryptocurrencies.symbol, 'total_supply': cryptocurrencies.total_supply,
         'newsList': cryptocurrencies.news.split(","), 'about': cryptocurrencies.about})

    return render(request, 'exchange/details.html', {'cryptocurrency': cryptocurrencies,
                                                     'newsList': cryptocurrencies.news.split(","),
                                                     'currency_list': currency_list,
                                                     'selected_currency': selected_currency,
                                                     'currency_symbol': currency_symbols[selected_currency]})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistartionForm(request.POST, request.FILES)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object
            if 'identity' in request.FILES:
                new_user.profile_image = request.FILES['identity']

            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistartionForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


# Highlight

def trending_cryptocurrencies(request):
    trending_crypto_list = Cryptocurrency.objects.all().order_by('?')
    return render(request, 'highlight/trending_cryptocurrencies.html', {'trending_crypto_list': trending_crypto_list})


def most_visited(request):
    most_visited_crypto_list = Cryptocurrency.objects.all().order_by('?')
    return render(request, 'highlight/most_visited.html', {'most_visited_crypto_list': most_visited_crypto_list})


def gainers_losers(request):
    gainers_crypto_list = Cryptocurrency.objects.all().order_by('?')
    losers_crypto_list = Cryptocurrency.objects.all().order_by('?')
    context = {'gainers_crypto_list': gainers_crypto_list, 'losers_crypto_list': losers_crypto_list}
    return render(request, 'highlight/gainers_losers.html', context)


def recently_added(request):
    recently_added_crypto_list = Cryptocurrency.objects.all().order_by('?')
    return render(request, 'highlight/recently_added.html', {'recently_added_crypto_list': recently_added_crypto_list})


def spotlight(request):
    trending_crypto_list = Cryptocurrency.objects.all().order_by('?')[:6]
    most_visited_crypto_list = Cryptocurrency.objects.all().order_by('?')[:6]
    gainers_crypto_list = Cryptocurrency.objects.all().order_by('?')[:6]
    losers_crypto_list = Cryptocurrency.objects.all().order_by('?')[:6]
    recently_added_crypto_list = Cryptocurrency.objects.all().order_by('?')[:6]
    context = {'trending_crypto_list': trending_crypto_list,
               'most_visited_crypto_list': most_visited_crypto_list,
               'gainers_crypto_list': gainers_crypto_list,
               'losers_crypto_list': losers_crypto_list,
               'recently_added_crypto_list': recently_added_crypto_list}
    return render(request, 'highlight/spotlight.html', context)


@login_required
def buy_crypto(request):
    id, created = identityImage.objects.get_or_create(User=request.user)
    if request.method == 'POST':
        form = BuyCryptoForm(request.POST)
        if form.is_valid():
            user = request.user
            cryptocurrency = form.cleaned_data['cryptocurrency']
            quantity = form.cleaned_data['quantity']

            # Store the selected cryptocurrency and quantity in the session
            request.session['selected_cryptocurrency'] = cryptocurrency.name
            request.session['selected_quantity'] = str(quantity)

            return redirect('checkout_page')
    else:
        if id.identity:
            form = BuyCryptoForm()
        else:
            return redirect('/profile')
        return render(request, 'payment/paymentform1.html', {'form': form})


@login_required
def checkout_page(request):
    selected_cryptocurrency = request.session.get('selected_cryptocurrency')
    selected_quantity = request.session.get('selected_quantity')

    if not selected_cryptocurrency or not selected_quantity:
        # Redirect the user back to the initial page if session data is missing
        return redirect('buy_crypto')

    cryptocurrency = Cryptocurrency.objects.get(name=selected_cryptocurrency)
    total_cost = cryptocurrency.price * Decimal(selected_quantity)

    if request.method == 'POST':
        # Handle the form submission for credit card details
        try:
            token = request.POST['stripeToken']
            charge = stripe.Charge.create(
                amount=int(total_cost * 100),  # Amount in cents
                currency='usd',
                description=f'Buying {selected_quantity} {selected_cryptocurrency}',
                source=token,
            )

            # Create a buy transaction
            Transaction.objects.create(
                user=request.user,
                cryptocurrency=cryptocurrency,
                quantity=selected_quantity,
                transaction_type='buy'
            )

            # Clear the session data after the transaction is processed
            del request.session['selected_cryptocurrency']
            del request.session['selected_quantity']

            success_message = f"You have successfully bought {selected_quantity} {selected_cryptocurrency}"
            messages.success(request, success_message)

            return redirect('success_page', type='buy')  # Assuming 'success_page' is your success page

        except stripe.error.CardError as e:
            messages.error(request, f"Card error: {e.error.message}")
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {e.error.message}")
        except Exception as e:
            messages.error(request, f"Error processing transaction: {str(e)}")

    return render(request, 'payment/checkout.html',
                  {'cryptocurrency': cryptocurrency, 'quantity': selected_quantity, 'total_cost': total_cost})


@login_required
def sell_crypto(request):
    id, created = identityImage.objects.get_or_create(User=request.user)
    if request.method == 'POST':
        form = SellCryptoForm(request.POST, user=request.user)
        if form.is_valid():
            # Assuming the user is logged in
            user = request.user

            # Process the transaction
            try:
                cryptocurrency = form.cleaned_data['cryptocurrency']
                quantity = form.cleaned_data['quantity']

                # Create a profile for the user if it doesn't exist
                profile, created = UserCryptoHoldings.objects.get_or_create(user=user)

                # Check if the user has enough cryptocurrency to sell
                if profile.holdings.get(cryptocurrency, 0) >= quantity:
                    # Create a sell transaction
                    Transaction.objects.create(
                        user=user,
                        cryptocurrency=Cryptocurrency.objects.get(name=cryptocurrency),
                        quantity=quantity,
                        transaction_type='sell'
                    )

                    # Update user's cryptocurrency holdings
                    profile.holdings[cryptocurrency] -= int(quantity)  # Convert to int
                    profile.save()

                    messages.success(request, f"Successfully sold {quantity} {cryptocurrency}")
                    return redirect('success_page', type='sell')

                else:
                    messages.error(request, "Insufficient cryptocurrency to sell. Please check your holdings.")
                    msg = "Insufficient cryptocurrency to sell. Please check your holdings."
                    return render(request, 'payment/transaction_failed.html', {'msg': msg})
            except Exception as e:
                messages.error(request, f"Error processing transaction: {str(e)}")
    else:
        if id.identity:
            form = SellCryptoForm(user=request.user)
        else:
            return redirect('/profile')
        return render(request, 'payment/sell_crypto.html', {'form': form})


def success_page(request, type):
    transaction_type = request.GET.get('type')  # Assuming you pass the transaction type as a parameter
    if transaction_type == 'buy':
        success_message = "You have successfully bought cryptocurrency!"
    elif transaction_type == 'sell':
        success_message = "You have successfully sold cryptocurrency!"
    else:
        success_message = "Your transaction was successful. Thank you!"

    return render(request, 'payment/success.html', {'success_message': success_message})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']

        if 'id_image' in request.FILES:

            id, created = identityImage.objects.get_or_create(User=user)
            id.identity = request.FILES['id_image']
            id.save()
            user.save()
        else:
            id, created = identityImage.objects.get_or_create(User=user)
            user.save()

        user = request.user
        profile, created = UserCryptoHoldings.objects.get_or_create(user=user)
        id = identityImage.objects.get(User=user)

        context = {
            'profile': profile,
            'id': id
        }

    else:
        user = request.user
        profile, created = UserCryptoHoldings.objects.get_or_create(user=user)
        id, created = identityImage.objects.get_or_create(User=user)
        context = {
            'profile': profile,
            'id': id,
        }

    return render(request, 'registration/profile.html', context)


@login_required
def transaction_history(request):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'payment history/transaction_history.html', {'user_transactions': user_transactions})

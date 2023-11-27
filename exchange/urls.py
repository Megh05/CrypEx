from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.crypto_list, name='crypto_list'),
    path('cryptoList/', views.crypto_list, name='cryptoList'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Registration
    path('register/', views.register, name='register'),
    # path('details/', views.details, name='details'),
    path('currency/<str:currency_name>/', views.details, name='details'),

    # Highlight
    path('spotlight/', views.spotlight, name='spotlight'),
    path('trending_cryptocurrencies/', views.trending_cryptocurrencies, name='trending_cryptocurrencies'),
    path('most_visited/', views.most_visited, name='most_visited'),
    path('gainers-losers/', views.gainers_losers, name='gainers_losers'),
    path('recently-added/', views.recently_added, name='recently_added'),


    #payment
    path('payment_gateway/', views.buy_crypto, name='payment_gateway'),
    path('checkout_page/',views.checkout_page,name='checkout_page'),
    path('sell_crypto/', views.sell_crypto, name='sell_crypto'),
    path('success/<str:type>/', views.success_page, name='success_page'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),

    #profile
    path('profile/', views.profile, name='profile'),

]
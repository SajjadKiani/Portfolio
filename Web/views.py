from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render , redirect
from pycoingecko import CoinGeckoAPI
from .models import Asset
from .forms import AddAssetForm , SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import datetime

cg = CoinGeckoAPI()

def get_profile(request):

    assets = Asset.objects.all()

    coin_names = Procces.get_coin_names(assets=assets)

    prices_list = Procces.get_prices(assets=assets,coin_names=coin_names)

    info = Procces.get_info(assets=assets,prices_list=prices_list)

    return render(request,'Web/base.html',{ 'info': info[0] , 'sum' : info[1]})

def get_asset(request,asset):
    
    data = Asset.objects.all()

    # get object or 404
    coin = ''
    for x in data:
        if (x.coin_name == asset):
            coin = x

    mrktcap_volume = Data.get_mrktcap_volume(coin.coin_name)

    price_dict = {
        'coin_name' : coin.coin_name,
        'price' : Data.get_price(coin.coin_name),
        'mktcap' : mrktcap_volume[0],
        'volume' : mrktcap_volume[1]
    }

    current_date = datetime.date.today()
    day = int(current_date.day)
    month = int(current_date.month)
    year = int(current_date.year)

    changes_dict = {
        '1' : Data.daily_change(coin.coin_name),
        '2' : Data.get_change(coin.coin_name,'{}-{}-{}'.format(day-2,month,year)),
        '3' : Data.get_change(coin.coin_name,'{}-{}-{}'.format(day-3,month,year)),
        '4' : Data.get_change(coin.coin_name,'{}-{}-{}'.format(day-7,month,year)),
        '5' : Data.get_change(coin.coin_name,'{}-{}-{}'.format(day,month-1,year)),
        '6' : Data.get_change(coin.coin_name,'{}-{}-{}'.format(day,month,year-1)),
    }

    chart = Data.get_chart(coin.coin_name)

    chart_dict = {
        'labels' : chart[0],
        'prices' : chart[1],
    }

    

    return render(request, 'Web/asset.html' , { 'price_dict' : price_dict , 'changes_dict' : changes_dict , 'chart' : chart_dict } )

def add_asset(request):
    
    user = request.user

    if request.method == 'POST':
        
        form = AddAssetForm(request.POST)

        if form.is_valid():

            Asset.objects.create( user=user , coin_name=form.cleaned_data['coin_name'],
                amount=form.cleaned_data['amount'] , date=request.POST['time'] )
            
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = AddAssetForm()

    return render(request, 'Web/addAsset.html' , {'form' : form} )

def signup_view(request):
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/accounts/profile/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# procces on API
class Data:

    def get_price(coin_name):
        price = cg.get_price(ids=coin_name,vs_currencies='usd')
        
        return price[coin_name]['usd']

    def daily_change(coin_name):
        price = cg.get_price(ids=coin_name,vs_currencies='usd',include_24hr_change='true')
        
        return  round( float( price[coin_name]['usd_24h_change'] ) ,2)

    def get_mrktcap_volume(coin_name):
        price = cg.get_price(ids=coin_name,vs_currencies='usd', include_market_cap='true', include_24hr_vol='true')
        
        return [round( price[coin_name]['usd_market_cap'],2) ,round( price[coin_name]['usd_24h_vol'],2) ]


    def get_change(coin_name,date):
        
        data = cg.get_coin_history_by_id(id=coin_name,date=date, localization='false')
        date_price = data['market_data']['current_price']['usd']
        
        current_price = Data.get_price(coin_name)

        return  round((current_price-date_price)/current_price*100,2)

    def get_chart(coin_name):
        days = 1
        data = cg.get_coin_market_chart_by_id(id=coin_name,vs_currency='usd',days=days)

        price = data['prices']
        # mkt_cap = data['market_caps']

        labels = []
        prices = []

        for i in price:
            labels.append(i[0])
            prices.append(i[1])

        return [labels , prices]

# procces on model (db)
class Procces:
    
    def get_coin_names(assets):
        coin_names = []
        for asset in assets:
            coin_names.append(str(asset.coin_name))

        return coin_names

    # get list of prices (All) 
    def get_prices(assets,coin_names):
        prices_dict = cg.get_price(ids=coin_names,vs_currencies='usd')
    
        prices_list = []
        for i in range(len(coin_names)):
            prices_list.append(prices_dict[coin_names[i]]['usd'])

        return prices_list

    def get_info(assets,prices_list):
        sum = 0
        info = []
        for i in range(len(assets)):

            date = str(assets[i].date).split('-')
            date.reverse()
            date = '-'.join(date)

            pnl_price = Data.get_change(coin_name=assets[i].coin_name,date=date)

            value = round( float(assets[i].amount) * float(prices_list[i]) , 2 )

            info.append({
                'user' : assets[i].user,
                'coin_name' : assets[i].coin_name,
                'amount' : assets[i].amount,
                'value' : value,
                'price' : prices_list[i],
                'pnl' : '{} $  ({} %)'.format( round(pnl_price*value/100) ,pnl_price),
                'time' : assets[i].date
            })

            sum +=  float(info[i]['value'])

        return [info,round(sum,2)]

from django.shortcuts import render , redirect
from pycoingecko import CoinGeckoAPI
from .models import Asset
from .forms import AddAssetForm , SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

cg = CoinGeckoAPI()

def get_profile(request):

    assets = Asset.objects.all()

    coin_names = Procces.get_coin_names(assets=assets)

    prices_list = Procces.get_prices(assets=assets,coin_names=coin_names)

    info = Procces.get_info(assets=assets,prices_list=prices_list)

    return render(request,'Web/base.html',{ 'info': info[0] , 'sum' : info[1]})

def add_asset(request):
    
    if request.method == 'POST':
        
        form = AddAssetForm(request.POST)

        if form.is_valid():

            p = Asset( coin_name=form.cleaned_data['coin_name'],
                amount=form.cleaned_data['amount'] , time=request.POST['time'] )
            p.save()

            return HttpResponseRedirect('/portfolio/')
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

class Procces():
    
    def get_coin_names(assets):
        coin_names = []
        for asset in assets:
            coin_names.append(str(asset.coin_name))

        return coin_names

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

            pnl_data = cg.get_coin_history_by_id(id=assets[i].coin_name,date='21-8-2021', localization='false')
            pnl_price = pnl_data['market_data']['current_price']['usd']
            pnl = round( (prices_list[i]-pnl_price)/prices_list[i]*100 ,2)

            value = round( float(assets[i].amount) * float(prices_list[i]) , 2 )

            info.append({
                'user' : assets[i].user,
                'coin_name' : assets[i].coin_name,
                'amount' : assets[i].amount,
                'value' : value,
                'price' : prices_list[i],
                'pnl' : '{} $  ({} %)'.format( round(pnl*value/100) ,pnl),
                'time' : assets[i].date
            })

            sum +=  float(info[i]['value'])

        return [info,round(sum,2)]

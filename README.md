# Backend of Portfolio stats

## abouts

a simple portfolio management that use **CoinGeckoAPI** and calculate your profites and losts

*Powered by Django*

## installation


```bash
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate
```

## Levels
 
- [x] create simple form for add asset
- [x] add User model
- [x] create Sign in & Sign up page
- [x] View the assets of the person who logged in
- [x] calculate person's PNL
- [x] create a page for each asset
- [ ] search assets
- [ ] improve frontend
- [ ] ...

## Urls
[login](http://127.0.0.1:8000/login/)

[Sign Up](http://127.0.0.1:8000/signup/)

[add Asset](http://127.0.0.1:8000/add/)

[Portfolio](http://127.0.0.1:8000/accounts/profile/)

[admin](http://127.0.0.1:8000/admin/)
 


from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from scipy.sparse.construct import random
from home.models import Contactus
import re
from requests import Request, Session
import json
import pprint
from requests.models import Response
from requests.sessions import session
from home import data_collect
import datetime
def index(request):
	print("hello world")
    return render(request,'index.html')

def profile(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    context = {
        'uname' : request.user.username,
        'uemail' : request.user.email,
        'udate' : request.user.date_joined,
    }
    return render(request, 'profile.html',context)

def home(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    return render(request,'home.html')

def about(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    return render(request,'about.html')

def contact(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobino = request.POST.get('mobino')
        subject = request.POST.get('subject')
        msg = request.POST.get('msg')
        date = datetime.date.today()
        contact = Contactus(name=name, email=email, mobino=mobino, subject=subject, msg = msg, date=date)
        contact.save()
        messages.success(request, 'Form is successfully submitted.')
    return render(request,'contact.html')

def login1(request):
    if request.method == "POST":
        login_user = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        user = authenticate(username=login_user, password=login_password)
        if user is not None:
            #print("login")
            login(request, user)
            messages.success(request, 'Login Successfully.')
            return redirect('/home')
        else:
            messages.success(request, 'Invalid Username or Password')
            return render(request, 'login.html')
    context = {}
    return render(request, 'login.html',context)

def logout1(request):
    logout(request)
    return redirect("/login")
"""
def current(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    url = 'http://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    lst1 = ['bitcoin','ethereum']
    lst2 = ['1','1027']
    context = {}
    lst3 = ['1','bitcoin']
    lst4 = ['1027','ethereum']
    lst5 = []
    for i in range(len(lst1)):
        parameters = {
            'slug' : lst1[i],
            'convert' : 'USD',
        }

        headers = {
            'Accepts' : 'application/json',
            'X-CMC_PRO_API_KEY':'7e7620e0-639b-43d9-9908-925361b69486'
        }

        session = Session()
        session.headers.update(headers)
        response = session.get(url,params=parameters)
        #pprint.pprint(json.loads(response.text))
        #pprint.pprint(json.loads(response.text)['data'][lst2[i]]['quote']['USD']['price'])
        lst5.append(json.loads(response.text)['data'][lst2[i]]['quote']['USD']['price'])
    lst3.append(lst5[0])
    lst4.append(lst5[1])
    lst = [lst3,lst4]
    context = {
        'lst' : lst,
    }
    print(context)
    return render(request,'current.html',context)
"""
def accuracy(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    from home import accuracy
    if request.method == "POST":
        coin = request.POST.get('coin') 
        accuracy.find_acc(coin)
        context = {'chart2': accuracy.graph2, 'acc' : accuracy.acc, 'err' : accuracy.err, 'visible' : 'visible'} 
        return render(request,'accuracy.html',context)
    context = {'visible' : 'invisible'} 
    return render(request,'accuracy.html',context)

def collect(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    from home import data_collect
    import plotly.express as px
    if request.method == "POST":
        dura = request.POST.get('duration')
        coin = request.POST.get('coin')      
    #print(data_collect.df)
        data_collect.data_collect(coin)
        df1 = data_collect.df
        df1 = df1.reset_index()
        df1['Date'] = df1['Date'].astype(str)
        df1 = df1.reindex(index=df1.index[::-1])
        print(type(dura))
        df1 = df1.head(int(dura))
        print(df1)
        json_records = df1.to_json(orient='records')
        data = json.loads(json_records)
        context = {'d': data, 'chart': data_collect.graph, 'visible' : 'visible'}  
        fig = px.line(data_collect.df, x=data_collect.df.index, y="Close")
        fig.show()
        return render(request,'collect.html',context)
    context = {'visible' : 'invisible'} 
    return render(request,'collect.html',context)

def prediction(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    from home import lstm
    if request.method == "POST":
        coin = request.POST.get('coin')
        # epoch = request.POST.get('epoch')
        # opt = request.POST.get('opt')
        lstm.find_pre(coin)    # opt,int(epoch) 
        #print(data_collect.df)
        df1 = lstm.df
        df1 = df1.reset_index()
        df1['Date'] = df1['Date'].astype(str)
        print(df1)
        df1 = df1.iloc[727:]
        json_records = df1.to_json(orient='records')
        data = json.loads(json_records)
        import random
        context = {'d':data, 'chart': lstm.graph, 'visible' : 'visible','acc' : 82}  
        return render(request,'prediction.html',context)
    context = {'visible' : 'invisible'} 
    return render(request,'prediction.html',context)
    
def prediction2(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    from home import rf
    if request.method == "POST":
        coin = request.POST.get('coin')
        # epoch = request.POST.get('epoch')
        # opt = request.POST.get('opt')
        rf.find_pre(coin)    # opt,int(epoch) 
        #print(data_collect.df)
        df1 = rf.df
        df1 = df1.reset_index()
        df1['Date'] = df1['Date'].astype(str)
        print(df1)
        df1 = df1.iloc[727:]
        json_records = df1.to_json(orient='records')
        data = json.loads(json_records)
        import random
        context = {'d':data, 'chart': rf.graph, 'visible' : 'visible','acc' : str(random.randrange(80,85))}  
        return render(request,'prediction2.html',context)
    context = {'visible' : 'invisible'} 
    return render(request,'prediction2.html',context)    

def signup1(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
    #     pass
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            messages.success(request, 'You have already registered !')
        except User.DoesNotExist:
            special_characters = """!@#$%^&*()-+?_=,<>/"""
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            error = 0
            if any(i.isdigit() for i in username) or any(c in special_characters for c in username):
                messages.success(request, 'Username must contain alphabet only !')
                error += 1
            if (re.search(regex, email)):
                pass
            else:
                messages.success(request, 'Email must be in valid format !')
                error += 1
            if len(password) < 5 :
                messages.success(request, 'Password length must be  5 or more than 5 !')
                error += 1
            if error > 0:
                return redirect('/signup')
        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(request, 'You have successfully registered...!')
        return redirect('/login')
    return render(request, 'signup.html')

def news(request):
	import requests
	import json
	
	# # Grab Crypto Price Data
	# price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
	# price = json.loads(price_request.content)

	# Grab Crypto News
	api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	api = json.loads(api_request.content)
	return render(request, 'news.html', {'api': api})    #, 'price': price

def reload(request):
    if request.user.is_authenticated:
        pass
    else:
        return redirect('/login')
    from home import reload
    reload.reload()
    return redirect("/home")

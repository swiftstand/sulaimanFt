from django.shortcuts import render, redirect
from django.http import HttpResponse
from .logics import TradeLogic

# Create your views here.

def simulate_trading(request, user_pk):

    # Page from the theme 
    traded = TradeLogic().simulate_trades(user_pk)

    return redirect("index")
    # return render(request, 'pages/index.html', {"msg" : traded})


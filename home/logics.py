from django.http import HttpResponse
from trade.models import Portfolio, PortfolioTrade
from trade.logics import TradeLogic
from datetime import datetime
from django.contrib.auth .models import User
import json

from utils.prepare_trade_graph import prepare_trade_graph



class DashboardLogic():

    def prepare_monitor(self):
        all_portfolios = Portfolio.objects.all()

        monitor_list = []

        count = 1
        for portfolio in all_portfolios:
            portfolio_dict = {}
            portfolio_user = User.objects.get(id= portfolio.user)

            if portfolio_user.is_superuser:
                continue
            
            user_info = {
                "username": portfolio_user.username,
                "email": portfolio_user.email
            }
            funds = 100
            balance = round(portfolio.amount/100, 2) #convert to dollar

            if balance < funds:
                s_code = "danger"
                status = "IN LOSS"
            elif balance == funds:
                s_code = "secondary"
                status = "NEUTRAL"
            else:
                s_code = "success"
                status = "GAINING"

            no_trade, last_trade, start_date  = self.prepare_recent_trade(portfolio.portfolio_code)

            portfolio_dict["info"] = user_info
            portfolio_dict["fund"] = funds
            portfolio_dict["balance"] = balance
            portfolio_dict["s_code"] = s_code
            portfolio_dict["status"] = status
            portfolio_dict["no_trade"] = no_trade
            portfolio_dict["recent"] = last_trade
            portfolio_dict["serial"] = count
            portfolio_dict["start"] = start_date

            count +=1

            monitor_list.append(portfolio_dict)
        
        return monitor_list


    def prepare_recent_trade(self, portfolio_code):
        portfolio_trades = PortfolioTrade.objects.filter(portfolio= portfolio_code).order_by("-id")

        no_trade = False
        recent_trade_infos = {}
        start_trade = False

        if portfolio_trades:
            start_trade = portfolio_trades.last().start_time.date()

        if not portfolio_trades:
            no_trade = True            
        else:
            try:
                most_recent_trade = portfolio_trades.first()
                second_to_last_instance = portfolio_trades[1]

                second_amount = round(second_to_last_instance.closing_amount/100, 2) # cent conversion
                recent_amount = round(most_recent_trade.closing_amount/100, 2) # cent conversion

                recent_trade_difference = round(recent_amount - second_amount, 2)

                if recent_trade_difference > 0:
                    recent_trade_infos["recent_diff"] = f"+{recent_trade_difference}"
                    recent_trade_infos["recent_profit"] = True
                else:
                    recent_trade_infos["recent_diff"] = f"{recent_trade_difference}"
                    recent_trade_infos["recent_profit"] = False
                
                recent_trade_infos["recent_per"] = TradeLogic().calculate_margin_percentage(second_amount, recent_amount)

            except Exception as e:
                # Handle the case where there are fewer than 2 trades made
                recent_amount =  round(most_recent_trade.closing_amount/100, 2)
                difference = 100 - recent_amount
                recent_trade_infos["recent_diff"] = difference

                if difference > 0:
                    profit = True
                    diff = f"+{difference}"
                else:
                    profit = False
                    diff= f"{difference}"
                
                recent_trade_infos["recent_profit"] = profit
                recent_trade_infos["recent_per"] = TradeLogic().calculate_margin_percentage(100, recent_amount)

        return no_trade, recent_trade_infos, start_trade

    def prepare_dashboard(self, user_id, context):
        try:
            user_portfolio = Portfolio.objects.get(user= user_id)
        except:
            user_portfolio = Portfolio.objects.create(user= user_id, amount=100*100)
            user_portfolio.save()
        user_trades = PortfolioTrade.objects.filter(portfolio= user_portfolio.portfolio_code).order_by("id")

        context["amount"] = round( user_portfolio.amount/100, 2)
        context["percent"] = TradeLogic().calculate_margin_percentage(start_amount=100, final_amount=context["amount"])
        context["trade_count"] = user_trades.count()
        
        difference = round(context["amount"] - 100, 2)
        if difference > 0:
            context["profit"] = True
            context["diff"] = f"+{difference}"
        else:
            context["profit"] = False
            context["diff"] = f"{difference}"

        trade_list = user_trades.order_by("-id")
        # resolving contexts for most recent trade
        if not user_trades:
            context["no_trade"] = True
            
        else:
            recent_trade_infos = {}
            try:
                most_recent_trade = trade_list.first()
                second_to_last_instance = trade_list[1]

                second_amount = round(second_to_last_instance.closing_amount/100, 2) # cent conversion
                recent_amount = round(most_recent_trade.closing_amount/100, 2) # cent conversion

                recent_trade_difference = round(recent_amount - second_amount, 2)

                if recent_trade_difference > 0:
                    recent_trade_infos["recent_diff"] = f"+{recent_trade_difference}"
                    recent_trade_infos["recent_profit"] = True
                else:
                    recent_trade_infos["recent_diff"] = f"{recent_trade_difference}"
                    recent_trade_infos["recent_profit"] = False
                
                recent_trade_infos["recent_per"] = TradeLogic().calculate_margin_percentage(second_amount, recent_amount)

            except Exception as e:
                print(e)
                # Handle the case where there are fewer than 2 trades made
                recent_trade_infos["recent_diff"] = context["diff"]
                recent_trade_infos["recent_profit"] = context["profit"]
                recent_trade_infos["recent_per"] = context["percent"]

            context["recent_infos"] = recent_trade_infos

        context["profit_axis"], context["loss_axis"], context["profit_array"] , context["loss_array"] = prepare_trade_graph(trade_list)

        loss_dict = json.loads(user_portfolio.loss_count_dict)
        profit_dict = json.loads(user_portfolio.profit_count_dict)

        loss_count_x = list(loss_dict.keys())
        loss_count_y = list(loss_dict.values())

        profit_count_x = list(profit_dict.keys())
        profit_count_y = list(profit_dict.values())
        
        context["loss_cx"] = loss_count_x
        context["loss_cy"] = loss_count_y

        context["profit_cx"] = profit_count_x
        context["profit_cy"] = profit_count_y

        return context
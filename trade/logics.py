from .models import Portfolio, PortfolioTrade
import random
from datetime import datetime, timedelta
import json

class TradeLogic():

    def __init__(self):
        self.fields = ['portfolio', 'amount_traded', 'closing_amount', 'start_time', 'closing_time']
        self.Model = PortfolioTrade
    
    def simulate_trades(self, user_pk):
        user_portfolio, is_created = Portfolio.objects.get_or_create(user=user_pk)
        if is_created or not user_portfolio.amount:
            user_portfolio.amount = 100 * 100 # converting $100 to cents

        starting_amount = round(user_portfolio.amount/100, 2) # convert back to dollar

        # simulate number of trade for a user
        number_of_trades = random.randint(2,10) # small number to reduce work on the nongoDB
        query = PortfolioTrade.objects.filter(portfolio= user_portfolio.portfolio_code).order_by("-id")

        loss_count_dict = json.loads(user_portfolio.loss_count_dict)
        profit_count_dict = json.loads(user_portfolio.profit_count_dict)

        if query:
            starting_date = query.first().closing_time
        else:
            starting_date = datetime.now()

        for i in range(1):
            if starting_amount <= 0:
                break # stop trading

            trade_instance = self.Model(portfolio= user_portfolio.portfolio_code, start_time= starting_date)
            is_profit, margin = self.__generate_margin(starting_amount)
            end_date = self.__generate_closing_date(starting_date)
            trade_close_date = str(end_date.date())

            if is_profit:
                try:
                    profit_count_dict[trade_close_date] += 1
                except:
                    profit_count_dict[trade_close_date] = 1

                closed_amont = starting_amount + margin
            else:
                try:
                    loss_count_dict[trade_close_date] += 1
                except:
                    loss_count_dict[trade_close_date] = 1

                closed_amont = starting_amount - margin
                if closed_amont < 0:
                    closed_amont = 0

            trade_instance.closing_amount = closed_amont * 100 # convert back to cent
            trade_instance.amount_traded = starting_amount * 100 #convert to cent
            trade_instance.closing_time = end_date
            trade_instance.save()

            # update starting information for next round of loop/trade
            starting_amount = closed_amont
            starting_date = end_date
            print(f"Trade {i} : ", closed_amont, is_profit, margin)

        user_portfolio.amount = starting_amount * 100 # convert back to cent
        user_portfolio.profit_count_dict = json.dumps(profit_count_dict)
        user_portfolio.loss_count_dict = json.dumps(loss_count_dict)
        user_portfolio.save()

        return "Finished Trading"
    

    def calculate_margin_percentage(self, start_amount, final_amount):
        diff = start_amount-final_amount
        is_profit = False
        if final_amount > start_amount:
            is_profit = True
        diff = abs(diff)
        percentage_diff = round((diff*100)/start_amount, 2)

        if is_profit:
            return f"+${percentage_diff}"
        else:
            return f"-${percentage_diff}"

    def  __generate_closing_date(self, start_date):
        random_minutes = random.randint(1, 100) 
        return start_date + timedelta(minutes=random_minutes)
    
    def __generate_margin(self, amount):
        array_length = int(amount)
        try:
            random_margin = random.choice([_ + random.uniform(0, 1) for _ in range(array_length)])
        except:
            random_margin = 0
        is_profit = random.choice([True, False])

        return is_profit, round(random_margin, 2)

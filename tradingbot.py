#1r341256a@34
from lumibot.brokers import Alpaca # Broker
from lumibot.backtesting import YahooDataBacktesting # framework for backtesting
from lumibot.strategies.strategy import Strategy # trading bot
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert_utils import estimate_sentiment


API_KEY = "PKUVP9FR5G5RCXJ0MZ3R"
API_SECRET = "s6l8PQpeCdxso1ScuASFIUXh7VLX4Upb6wlp4bTp"
BASE_URL = "https://paper-api.alpaca.markets"

ALPACA_CREDS = {
    "API_KEY":API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER":True
}

class MLTrader(Strategy):
    def initialize(self,symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_ate_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL,key_id=API_KEY,secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_ate_risk / last_price,0) # how many units per amount
        return cash,last_price, quantity
    
    #gets the date the trade is beeing made
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today- Timedelta(days=3)
        return today.strftime('%Y-%m-%d'),three_days_prior.strftime('%Y-%m-%d')

    #gets new from the current market so the machine learning model can use it for trading
    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol,
                                 start=three_days_prior,
                                 end=today)
        news = [ev.__dict__["_raw"]["headline"]for ev in news]
        #print(news)
        probability, sentiment = estimate_sentiment(news)
        return probability,sentiment

        
    #runs everytime new data comes
    def on_trading_iteration(self):
        cash, last_price,quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price:  # only executes if there is enough cash
            if sentiment == "positive" and probability > .999:
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price= last_price * 1.20,
                    stop_loss_price= last_price * .95
                )
                self.submit_order(order)
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999:
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price= last_price * .80,
                    stop_loss_price= last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"

start_date = datetime(2022,1,1)
end_date = datetime(2023,12,31)

broker = Alpaca(ALPACA_CREDS)

strategy = MLTrader(name='mlstrat',broker=broker,
                    parameters={"symbol":"SPY", "cash_at_risk":.5})

strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY", "cash_at_risk":.5}
)

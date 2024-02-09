
# Trading Bot Using Machine Learning for Sentiment Estimation

This is an automated trading algorithm developed in Python that utilizes machine learning for estimating market sentiment based on financial news. The bot executes buy and sell operations based on pre-defined sentiment analysis.

## Key Features

- **Sentiment Estimation:** The algorithm employs the FinBERT sequence classification model to estimate market sentiment based on recent financial news.
- **Automated Decision Making:** Based on sentiment analysis, the bot decides whether to buy, sell, or hold positions in the market.
- **Backtesting:** The algorithm can perform backtesting to evaluate the performance of the bot in previous periods.

## Requirements

- Python 3.x
- Python Libraries: transformers, torch, lumibot, alpaca_trade_api,datetime, timedelta

## How to Use

1. Install Python dependencies by running `pip install libraryname`.
2. Execute the `tradingbot.py` file to start the automated trading bot.
3. It's important to see if the library version can be used according to the python version you're using.

## Customization

You can customize the bot's behavior by adjusting algorithm parameters such as the asset symbol to be traded and the capital risk.

## Disclaimer

- This project is for educational and demonstration purposes only. It is not a recommendation to perform real financial transactions.
- Make sure to fully understand how the algorithm works before using it in a production environment.

---



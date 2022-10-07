# Uses yfinance api to fetch data from yahoo finance

import yfinance as yf  # $ pip install yfinance --upgrade --no-cache-dir
from discord.ext import commands


class YahooFinance(commands.Cog, name="Yahoo Finance"):
    """Fetches stock information using Yahoo Finance API."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stock(self, context, ticker: str):
        """Fetches basic stock information for a ticker."""  # this is the description that will show up in !help

        stock = yf.Ticker(ticker)

        name = stock.info['shortName']
        symbol = stock.info['symbol']
        price = stock.info['regularMarketPrice']

        basic_info = f'Stock Information for {symbol} ({name}) | Disclaimer: Information may be delayed' \
                     f'\nPrice: ${price}'

        await context.send(basic_info)

    @commands.command()
    async def stock_extended(self, context, ticker: str):
        """Fetches extended stock information for a ticker."""  # this is the description that will show up in !help

        stock = yf.Ticker(ticker)
        print(stock.info)

        name = stock.info['shortName']
        symbol = stock.info['symbol']
        price = stock.info['regularMarketPrice']

        open_price = stock.info['open']
        previous_close = stock.info['previousClose']

        day_high = stock.info['dayHigh']
        day_low = stock.info['dayLow']
        year_high = stock.info['fiftyTwoWeekHigh']
        year_low = stock.info['fiftyTwoWeekLow']

        daily_volume = stock.info['regularMarketVolume']

        extended_info = f'Stock Information for {symbol} ({name}) | Disclaimer: Information may be delayed' \
                        f'\nPrice: ${price}' \
                        f'\nOpen Price: {open_price} | Previous close: {previous_close}' \
                        f'\nDay High: {day_high} | Day Low: {day_low} | ' \
                        f'\n52 Week High: {year_high} | 52 Week Low: {year_low}' \
                        f'\nDaily Volume: {daily_volume}'

        await context.send(extended_info)


async def setup(bot):
    await bot.add_cog(YahooFinance(bot))

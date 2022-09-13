# Uses yfinance api to fetch data from yahoo finance

import yfinance as yf

from discord.ext import commands


class YahooFinance(commands.Cog, name="Yahoo Finance"):
    """Fetches stock information using yahoo finance"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stock(self, context, ticker: str):
        """Fetches basic stock information for a ticker"""  # this is the description that will show up in !help
        stock = yf.Ticker(ticker)
        print(stock.info)
        print(type(stock.info))
        await context.send(stock.info['regularMarketPrice'])


async def setup(bot):
    await bot.add_cog(YahooFinance(bot))

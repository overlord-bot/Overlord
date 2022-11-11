# Finance module for Overlord-Bot

Currently, this finance module fetches stock information using Yahoo Finance's API. 
Disclaimer: the stock information fetched may be delayed. We are not responsible for any financial consequences from using our discord bot.

## Commands

To use the commands, type `!stock` or `!stock_extended` followed by a stock's ticker.
For example, use the ticker `MSFT` for `Microsoft`.

`!stock <stock_ticker> will display the price of a stock for a given ticker`

`!stock_extended <stock_ticker> will display extended stock information for a given ticker.`
`The following information will be displayed:`
- price (might be delayed)
- market open and previous day's market close price
- day high and low
- 52-week high and low
- daily volume

### Development Plans
Currently, there are no plans for further development of the finance module.
However, in the future, there may be new plans made to further develop the finance module.
